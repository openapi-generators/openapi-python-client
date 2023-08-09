"""Abstract base class for API resources."""

from __future__ import annotations

import abc
import copy
import logging
import time
import typing as t
from http import HTTPStatus
from urllib.parse import urlparse

import backoff
import requests
from dlt.sources.helpers.requests import Client

from dlt.common import logger
from . import metrics
from .authenticators import APIAuthenticator
from .exceptions import FatalAPIError, RetriableAPIError
from .jsonpath import extract_jsonpath
from .paginators import (
    BaseAPIPaginator,
    BaseOffsetPaginator,
    SimpleHeaderPaginator,
    SinglePagePaginator,
)

if t.TYPE_CHECKING:
    from backoff.types import Details


DEFAULT_PAGE_SIZE = 1000
DEFAULT_REQUEST_TIMEOUT = 300  # 5 minutes

TPaginatorToken = t.TypeVar("TPaginatorToken")
TEndpoint = t.TypeVar("TEndpoint", bound="RestAPIEndpoint", covariant=True)
TPaginator = t.TypeVar("TPaginator", bound="BaseAPIPaginator", covariant=True)
TAuthenticator = t.TypeVar("TAuthenticator", bound="APIAuthenticator", covariant=True)
TDefEndpoint = t.TypeVar("TDefEndpoint", bound="RestAPIEndpoint")
TDefPaginator = t.TypeVar("TDefPaginator", bound="BaseAPIPaginator")
TDefAuthenticator = t.TypeVar("TDefAuthenticator", bound="APIAuthenticator")

# add covariant
# overloads for ALL paginators
# overloads for ALL authenticators


class BaseAPIEndpointFactory:
    pass


class BaseAPIEndpoint:
    pass


class RestAPIEndpoint(BaseAPIEndpoint, t.Generic[TPaginatorToken]):
    """Base class for a REST API endpoint."""

    records_jsonpath: str | None = None

    def __init__(
        self,
        api: RestAPIEndpointFactory,
        path: str,
        records_jsonpath: str | None = None,
        method: str = "GET",
        paginator: BaseAPIPaginator | None = None,
        http_headers: dict[str, str] | None = None,
        request_body: dict | None = None,
        request_params: dict | None = None,
    ) -> None:
        self.api = api
        self.path = path
        # If records_jsonpath is provided at init, use it
        if records_jsonpath:
            self.records_jsonpath = records_jsonpath
        # Otherwise, use the class-level records_jsonpath
        if not self.records_jsonpath:
            # If the class-level records_jsonpath is None, use the default from the API
            self.records_jsonpath = api.records_jsonpath
        self.method = method
        if paginator:
            paginator = copy.deepcopy(paginator)
        self.paginator = paginator or copy.deepcopy(api.default_paginator)
        self.http_headers = api.headers
        self.http_headers.update(http_headers or {})
        self.request_body = request_body
        self.request_params = request_params

    @property
    def resolved_path(self) -> str:
        """Get entity URL."""
        return self.api.base_url + self.path

    def _request(self, prepared_request: requests.PreparedRequest) -> requests.Response:
        """Send a prepared request and return the response."""
        response = self.api.requests_session.send(prepared_request, timeout=self.timeout)
        self._write_request_duration_log(
            endpoint=self.path,
            response=response,
            extra_tags={"url": prepared_request.path_url},
        )
        self.api.validate_response(response)
        logger.debug("Response received successfully.")
        return response

    def get_request_params(
        self, next_page_token: TPaginatorToken | None
    ) -> dict[str, t.Any] | str | None:
        """Create or update the request params for the REST API request."""
        return self.request_params

    def get_request_body(self, next_page_token: TPaginatorToken | None) -> dict | None:
        """Create or update the request body for the REST API request."""
        return self.request_body

    def get_request_url(self, next_page_token: TPaginatorToken | None) -> str | None:
        """Create or update the request url for the REST API request."""
        return None

    def get_prepared_request(self, *args: t.Any, **kwargs: t.Any) -> requests.PreparedRequest:
        """Build a generic but authenticated request."""
        request = requests.Request(*args, **kwargs)
        return self.api.authenticator(self.api.requests_session.prepare_request(request))

    def prepare_request(self, next_page_token: TPaginatorToken | None) -> requests.PreparedRequest:
        """Prepare a request object for this endpoint."""
        http_method = self.method
        headers = self.http_headers

        url = self.get_request_url(next_page_token) or self.resolved_path
        params = self.get_request_params(next_page_token) or {}
        request_data = self.get_request_body(next_page_token)

        return self.get_prepared_request(
            method=http_method,
            url=url,
            params=params,
            headers=headers,
            json=request_data,
        )

    def request_records(self) -> t.Iterable[dict]:
        """Request records from REST endpoint(s), returning response records."""
        decorated_request = self.api.request_decorator(self._request)

        with metrics.http_request_counter("cdf", self.path) as request_counter:
            while not self.paginator.finished:
                prepared_request = self.prepare_request(
                    next_page_token=self.paginator.current_value
                )
                resp = decorated_request(prepared_request)
                request_counter.increment()
                self.update_sync_costs(prepared_request, resp)
                yield from self.parse_response(resp)
                self.paginator.advance(resp)

    def _write_request_duration_log(
        self, endpoint: str, response: requests.Response, extra_tags: dict | None
    ) -> None:
        """Write a log entry for the request duration."""
        extra_tags = extra_tags or {}
        point = metrics.Point(
            "timer",
            metric=metrics.Metric.HTTP_REQUEST_DURATION,
            value=response.elapsed.total_seconds(),
            tags={
                metrics.Tag.ENDPOINT: endpoint,
                metrics.Tag.HTTP_STATUS_CODE: response.status_code,
                metrics.Tag.STATUS: (
                    metrics.Status.SUCCEEDED
                    if response.status_code < HTTPStatus.BAD_REQUEST
                    else metrics.Status.FAILED
                ),
                **extra_tags,
            },
        )
        metrics.log(logger, point=point)

    def update_sync_costs(
        self, request: requests.PreparedRequest, response: requests.Response
    ) -> dict[str, int]:
        """Update internal calculation of sync costs."""
        call_costs = self.calculate_sync_cost(request, response)
        self._sync_costs = {
            k: self._sync_costs.get(k, 0) + call_costs.get(k, 0) for k in call_costs
        }
        return self._sync_costs

    def calculate_sync_cost(
        self, request: requests.PreparedRequest, response: requests.Response
    ) -> t.Dict[str, int]:
        """Calculate the cost of the last API call made."""
        return {}

    @property
    def timeout(self) -> int:
        """Return the request timeout limit in seconds."""
        return DEFAULT_REQUEST_TIMEOUT

    def get_records(self) -> t.Iterable[dict[str, t.Any]]:
        """Return a generator of record-type dictionary objects."""
        for record in self.request_records():
            transformed_record = self.post_process(record)
            if transformed_record is None:
                continue
            yield transformed_record

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records."""
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def post_process(self, row: dict) -> dict | None:
        """As needed, append or transform raw data to match expected structure."""
        return row

    def __iter__(self) -> t.Iterable[t.Dict[str, t.Any]]:
        """Lazily consume the endpoint and return a generator of records."""
        yield from self.get_records()

    def __call__(self) -> t.List[t.Dict[str, t.Any]]:
        """Immediately consume the endpoint and return a list of records."""
        return list(self)


class RestAPIEndpointFactory(
    BaseAPIEndpointFactory,
    t.Generic[TDefEndpoint, TDefPaginator, TDefAuthenticator],
    metaclass=abc.ABCMeta,
):
    """Abstract base class for REST APIs. This can be thought of as a api for endpoints."""

    extra_retry_statuses: t.Sequence[int] = [HTTPStatus.TOO_MANY_REQUESTS]
    """HTTP statuses that should be retried."""
    records_jsonpath: str = "$[*]"
    """JSONPath expression to extract records from the response."""
    endpoint_klass: t.Type[TDefEndpoint] = RestAPIEndpoint
    """The default endpoint class to use for this API."""
    paginator_klass: t.Type[TDefPaginator] = SinglePagePaginator
    """The default paginator class to use for this API."""
    default_paginator = SinglePagePaginator()
    """The default paginator instance to use for this API. 
    
    If no paginator is provided, a deepcopy of this one will be used.
    """
    authenticator: TDefAuthenticator | None = None
    """The authenticator to use for this API. 
    
    This can be overridden by passing an authenticator to the constructor. An authenticator
    is a callable that takes a prepared request and returns a prepared request. It is required.
    A ValueError will be raised if no authenticator is provided.
    """

    @property
    @abc.abstractmethod
    def base_url(self) -> str:
        """Return the base url, e.g. ``https://api.gong.io/v2/``."""

    def __init__(
        self,
        authenticator: APIAuthenticator | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        """Initialize the REST endpoint."""
        if authenticator:
            # Override the class-level authenticator with the provided one.
            self.authenticator = authenticator
        if self.authenticator is None:
            raise ValueError("No authenticator provided.")
        self.headers = headers or {}
        self.client = Client(session_attrs={"headers": self.headers})

    @property
    def requests_session(self) -> requests.Session:
        """Get requests session."""
        return self.client.session

    def validate_response(self, response: requests.Response) -> None:
        """Validate HTTP response."""
        if (
            response.status_code in self.extra_retry_statuses
            or HTTPStatus.INTERNAL_SERVER_ERROR <= response.status_code <= max(HTTPStatus)
        ):
            raise RetriableAPIError(self.response_error_message(response), response)
        if HTTPStatus.BAD_REQUEST <= response.status_code < HTTPStatus.INTERNAL_SERVER_ERROR:
            raise FatalAPIError(self.response_error_message(response))

    def response_error_message(self, response: requests.Response) -> str:
        """Build error message for invalid http statuses."""
        full_path = urlparse(response.url).path or self.base_url
        error_type = (
            "Client"
            if HTTPStatus.BAD_REQUEST <= response.status_code < HTTPStatus.INTERNAL_SERVER_ERROR
            else "Server"
        )
        return f"{response.status_code} {error_type} Error: {response.reason} for path: {full_path}"

    def request_decorator(self, func: t.Callable) -> t.Callable:
        """Instantiate a decorator for handling request failures."""
        decorator: t.Callable = backoff.on_exception(
            self.backoff_wait_generator,
            (
                ConnectionResetError,
                RetriableAPIError,
                requests.exceptions.ReadTimeout,
                requests.exceptions.ConnectionError,
                requests.exceptions.ChunkedEncodingError,
                requests.exceptions.ContentDecodingError,
            ),
            max_tries=self.backoff_max_tries,
            on_backoff=self.backoff_handler,
            jitter=self.backoff_jitter,
        )(func)
        return decorator

    @t.overload
    def endpoint_factory(
        self,
        path: str,
        klass: None = None,
        /,
        **kwargs,
    ) -> TDefEndpoint:
        ...

    @t.overload
    def endpoint_factory(
        self,
        path: str,
        klass: t.Type[RestAPIEndpoint],
        /,
        *,
        records_jsonpath: str | None = None,
        method: str = "GET",
        paginator: BaseAPIPaginator | None = None,
        http_headers: dict[str, str] | None = None,
        request_body: dict | None = None,
        request_params: dict | None = None,
    ) -> TEndpoint:
        ...

    @t.overload
    def endpoint_factory(
        self,
        path: str,
        klass: t.Type[TEndpoint],
        /,
        **kwargs,
    ) -> TEndpoint:
        ...

    def endpoint_factory(
        self, path: str, klass: t.Type[TEndpoint] | None = None, /, **kwargs
    ) -> TDefEndpoint | TEndpoint:
        """Return a new endpoint object. Kwargs are passed to the endpoint constructor."""
        return (klass or self.endpoint_klass)(api=self, path=path, **kwargs)

    @t.overload
    def paginator_factory(
        self,
        klass: None = None,
        /,
        **kwargs,
    ) -> TDefPaginator:
        ...

    @t.overload
    def paginator_factory(
        self,
        klass: t.Type[SinglePagePaginator],
        /,
    ) -> SinglePagePaginator:
        ...

    @t.overload
    def paginator_factory(
        self,
        klass: t.Type[SimpleHeaderPaginator],
        /,
        key: str,
    ) -> SimpleHeaderPaginator:
        ...

    @t.overload
    def paginator_factory(
        self,
        klass: t.Type[BaseOffsetPaginator],
        /,
        start_value: int,
        page_size: int,
    ) -> BaseOffsetPaginator:
        ...

    @t.overload
    def paginator_factory(
        self,
        klass: t.Type[TPaginator],
        /,
        **kwargs,
    ) -> TPaginator:
        ...

    def paginator_factory(
        self,
        klass: t.Type[TPaginator] | None = None,
        /,
        **kwargs,
    ) -> TDefPaginator | TPaginator:
        return (klass or self.paginator_klass)(**kwargs)

    def backoff_wait_generator(self) -> t.Generator[float, None, None]:
        """The wait generator used by the backoff decorator on request failure."""
        return backoff.expo(factor=2)

    def backoff_max_tries(self) -> int:
        """The number of attempts before giving up when retrying requests."""
        return 5

    def backoff_jitter(self, value: float) -> float:
        """Amount of jitter to add."""
        return backoff.random_jitter(value)

    def backoff_handler(self, details: "Details") -> None:
        """Adds additional behaviour prior to retry."""
        e = details.get("exception")
        if (
            isinstance(e, RetriableAPIError)
            and e.response.status_code == HTTPStatus.TOO_MANY_REQUESTS
        ):
            retry_after = int(e.response.headers.get("Retry-After", 15))
            logging.warning(
                "429 Too Many Requests: backing off %0.2f seconds after %d tries. Retry-After: %s",
                details.get("wait"),
                details.get("tries"),
                retry_after,
            )
            time.sleep(retry_after)
        else:
            logging.error(
                (
                    "Backing off %0.2f seconds after %d tries "
                    "calling function %s with args %s and kwargs "
                    "%s"
                ),
                details.get("wait"),
                details.get("tries"),
                details.get("target"),
                details.get("args"),
                details.get("kwargs"),
            )

    def backoff_runtime(self, *, value: t.Callable[[t.Any], int]) -> t.Generator[int, None, None]:
        """Optional backoff wait generator that can replace the default `backoff.expo`."""
        exception = yield  # type: ignore[misc]
        while True:
            exception = yield value(exception)


if __name__ == "__main__":

    class JsonPlaceholderAPIEndpoint(RestAPIEndpoint[None]):
        """JsonPlaceholder API endpoint."""

    class JsonPlaceholderAPIEndpointSpecialized(JsonPlaceholderAPIEndpoint):
        """JsonPlaceholder API endpoint specialized."""

    class JsonPlaceholderAPIFactory(
        RestAPIEndpointFactory[JsonPlaceholderAPIEndpoint, SinglePagePaginator, APIAuthenticator]
    ):
        """Factory for the JsonPlaceholder API."""

        base_url = "https://jsonplaceholder.typicode.com/"
        endpoint_klass = JsonPlaceholderAPIEndpoint
        paginator_klass = SinglePagePaginator
        default_paginator = SinglePagePaginator()
        authenticator = APIAuthenticator()
        records_jsonpath = "$.[*]"

    # Example usage with overloaded type signatures
    api = JsonPlaceholderAPIFactory()
    posts = api.endpoint_factory("posts")
    todos = api.endpoint_factory("todos")
    users = api.endpoint_factory("users")
