from typing import Iterator, Optional, List, Dict, Any, TypeVar, Iterable, cast, Literal
import copy
from urllib.parse import urlparse

from requests.auth import AuthBase
from requests import Session as BaseSession
from requests import Response, Request

from dlt.common import logger
from dlt.common import jsonpath
from dlt.sources.helpers.requests.retry import Client

from .typing import HTTPMethodBasic, HTTPMethod
from .paginators import BasePaginator
from .auth import AuthConfigBase
from .detector import create_paginator, find_records

from .utils import join_url


_T = TypeVar("_T")


class PageData(List[_T]):
    """A list of elements in a single page of results with attached request context.

    The context allows to inspect the response, paginator and authenticator, modify the request
    """

    def __init__(
        self,
        __iterable: Iterable[_T],
        request: Request,
        response: Response,
        paginator: BasePaginator,
        auth: AuthConfigBase,
    ):
        super().__init__(__iterable)
        self.request = request
        self.response = response
        self.paginator = paginator
        self.auth = auth


class RESTClient:
    """A generic REST client for making requests to an API.

    Attributes:
        base_url (str): The base URL of the API.
        headers (Optional[Dict[str, str]]): Headers to include in all requests.
        auth (Optional[AuthBase]): An authentication object to use for all requests.
        paginator (Optional[BasePaginator]): A paginator object for handling API pagination.
            Note that this object will be deepcopied for each request to ensure that the
            paginator state is not shared between requests.
    """

    def __init__(
        self,
        base_url: str,
        headers: Optional[Dict[str, str]] = None,
        auth: Optional[AuthConfigBase] = None,
        paginator: Optional[BasePaginator] = None,
        data_selector: Optional[jsonpath.TJsonPath] = None,
        session: BaseSession = None,
    ) -> None:
        self.base_url = base_url
        self.headers = headers
        self.auth = auth

        if session:
            self._validate_session_raise_for_status(session)
            self.session = session
        else:
            self.session = Client(raise_for_status=False).session

        self.paginator = paginator
        self.data_selector = data_selector

    def _validate_session_raise_for_status(self, session: BaseSession) -> None:
        # dlt.sources.helpers.requests.session.Session
        # has raise_for_status=True by default
        if getattr(self.session, "raise_for_status", False):
            logger.warning(
                "The session provided has raise_for_status enabled. "
                "This may cause unexpected behavior."
            )

    def _create_request(
        self,
        path: str,
        method: HTTPMethod,
        params: Dict[str, Any],
        json: Optional[Dict[str, Any]] = None,
        auth: Optional[AuthBase] = None,
        hooks: Optional[Dict[str, Any]] = None,
    ) -> Request:
        parsed_url = urlparse(path)
        if parsed_url.scheme in ("http", "https"):
            url = path
        else:
            url = join_url(self.base_url, path)

        return Request(
            method=method,
            url=url,
            headers=self.headers,
            params=params,
            json=json,
            auth=auth or self.auth,
            hooks=hooks,
        )

    def _send_request(self, request: Request) -> Response:
        logger.info(
            f"Making {request.method.upper()} request to {request.url}"
            f" with params={request.params}, json={request.json}"
        )

        prepared_request = self.session.prepare_request(request)

        return self.session.send(prepared_request)

    def request(
        self, path: str = "", method: HTTPMethod = "GET", **kwargs: Any
    ) -> Response:
        prepared_request = self._create_request(
            path=path,
            method=method,
            **kwargs,
        )
        return self._send_request(prepared_request)

    def get(
        self, path: str, params: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> Response:
        return self.request(path, method="GET", params=params, **kwargs)

    def post(
        self, path: str, json: Optional[Dict[str, Any]] = None, **kwargs: Any
    ) -> Response:
        return self.request(path, method="POST", json=json, **kwargs)

    def paginate(
        self,
        path: str = "",
        method: HTTPMethodBasic = "GET",
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        auth: Optional[AuthConfigBase] = None,
        paginator: Optional[BasePaginator] = None,
        data_selector: Optional[jsonpath.TJsonPath] = None,
        response_actions: Optional[List[Dict[str, Any]]] = None,
        hooks: Optional[Dict[str, Any]] = None,
    ) -> Iterator[PageData[Any]]:
        """Paginate over an API endpoint.

        Example:
            >>> client = APIClient(...)
            >>> for page in client.paginate("/search", method="post", json={"query": "foo"}):
            >>>     print(page)
        """
        paginator = paginator if paginator else copy.deepcopy(self.paginator)
        auth = auth or self.auth
        data_selector = data_selector or self.data_selector

        request = self._create_request(
            path=path, method=method, params=params, json=json, auth=auth, hooks=hooks
        )

        while True:
            response = self._send_request(request)

            if response_actions:
                action_type = self.handle_response_actions(response, response_actions)
                if action_type == "ignore":
                    logger.info(
                        f"Error {response.status_code}. Ignoring response '{response.json()}' and stopping pagination."
                    )
                    break
                elif action_type == "retry":
                    logger.info("Retrying request.")
                    continue

            if paginator is None:
                paginator = self.detect_paginator(response)

            data = self.extract_response(response, data_selector)
            paginator.update_state(response)
            paginator.update_request(request)

            # yield data with context
            yield PageData(
                data, request=request, response=response, paginator=paginator, auth=auth
            )

            if not paginator.has_next_page:
                break

    def extract_response(
        self, response: Response, data_selector: jsonpath.TJsonPath
    ) -> List[Any]:
        if data_selector:
            # we should compile data_selector
            data: Any = jsonpath.find_values(data_selector, response.json())
            # extract if single item selected
            data = data[0] if isinstance(data, list) and len(data) == 1 else data
        else:
            data = find_records(response.json())
        # wrap single pages into lists
        if not isinstance(data, list):
            data = [data]
        return cast(List[Any], data)

    def detect_paginator(self, response: Response) -> BasePaginator:
        paginator = create_paginator(response)
        if paginator is None:
            raise ValueError(
                f"No suitable paginator found for the response at {response.url}"
            )
        logger.info(f"Detected paginator: {paginator.__class__.__name__}")
        return paginator

    def handle_response_actions(
        self, response: Response, actions: List[Dict[str, Any]]
    ) -> Optional[str]:
        """Handle response actions based on the response and the provided actions.

        Example:
        response_actions = [
            {"status_code": 404, "action": "ignore"},
            {"content": "Not found", "action": "ignore"},
            {"status_code": 429, "action": "retry"},
            {"status_code": 200, "content": "some text", "action": "retry"},
        ]
        action_type = client.handle_response_actions(response, response_actions)
        """
        content = response.text

        for action in actions:
            status_code = action.get("status_code")
            content_substr: str = action.get("content")
            action_type: str = action.get("action")

            if status_code is not None and content_substr is not None:
                if response.status_code == status_code and content_substr in content:
                    return action_type

            elif status_code is not None:
                if response.status_code == status_code:
                    return action_type

            elif content_substr is not None:
                if content_substr in content:
                    return action_type

        return None
