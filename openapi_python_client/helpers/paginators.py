"""Generic paginator classes."""

from __future__ import annotations

import typing as t
from abc import ABCMeta, abstractmethod
from urllib.parse import ParseResult, urlparse

from .jsonpath import extract_jsonpath

if t.TYPE_CHECKING:
    from requests import Response


T = t.TypeVar("T")
TPageToken = t.TypeVar("TPageToken")


# TODO: move to common.utils
def first(iterable: t.Iterable[T]) -> T:
    """Return the first element of an iterable or raise an exception."""
    return next(iter(iterable))


class BaseAPIPaginator(t.Generic[TPageToken], metaclass=ABCMeta):
    """An API paginator object."""

    def __init__(self, start_value: TPageToken) -> None:
        """Create a new paginator."""
        self._value: TPageToken = start_value
        self._page_count = 0
        self._finished = False
        self._last_seen_record: dict | None = None

    @property
    def current_value(self) -> TPageToken:
        """Get the current pagination value."""
        return self._value

    @property
    def finished(self) -> bool:
        """Get a flag that indicates if the last page of data has been reached."""
        return self._finished

    @property
    def count(self) -> int:
        """Count the number of pages traversed so far."""
        return self._page_count

    def advance(self, response: Response) -> None:
        """Get a new page value and advance the current one."""
        self._page_count += 1

        if not self.has_more(response):
            self._finished = True
            return

        new_value = self.get_next(response)

        if new_value and new_value == self._value:
            raise RuntimeError(
                "Loop detected in pagination. Pagination token %s is identical to prior token."
                % new_value
            )

        if not new_value:
            self._finished = True
        else:
            self._value = new_value

    def has_more(self, response: Response) -> bool:
        """Override this method to check if the endpoint has any pages left."""
        return True

    @abstractmethod
    def get_next(self, response: Response) -> TPageToken | None:
        """Get the next pagination token or index from the API response."""
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}<{self.current_value}>"

    def __repr__(self) -> str:
        return str(self)


class SinglePagePaginator(BaseAPIPaginator[None]):
    """A paginator that works with single-page endpoints."""

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        """Create a new paginator."""
        super().__init__(None, *args, **kwargs)

    def get_next(self, response: Response) -> None:
        """Returns `None` to indicate the end of pagination."""
        return None


class BaseHATEOASPaginator(
    BaseAPIPaginator[t.Optional[ParseResult]],
    metaclass=ABCMeta,
):
    """Paginator class for APIs supporting HATEOAS links in their response bodies."""

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        """Create a new paginator."""
        super().__init__(None, *args, **kwargs)

    @abstractmethod
    def get_next_url(self, response: Response) -> str | None:
        """Override this method to extract a HATEOAS link from the response."""

    def get_next(self, response: Response) -> ParseResult | None:
        """Get the next pagination token or index from the API response."""
        next_url = self.get_next_url(response)
        return urlparse(next_url) if next_url else None


class HeaderLinkPaginator(BaseHATEOASPaginator):
    """Paginator class for APIs supporting HATEOAS links in their headers."""

    def get_next_url(self, response: Response) -> str | None:
        """Override this method to extract a HATEOAS link from the response."""
        url: str | None = response.links.get("next", {}).get("url")
        return url


class JSONPathPaginator(BaseAPIPaginator[t.Optional[str]]):
    """Paginator class for APIs returning a pagination token in the response body."""

    def __init__(self, jsonpath: str, *args: t.Any, **kwargs: t.Any) -> None:
        """Create a new paginator."""
        super().__init__(None, *args, **kwargs)
        self._jsonpath = jsonpath

    def get_next(self, response: Response) -> str | None:
        """Get the next page token."""
        matches = extract_jsonpath(self._jsonpath, response.json())
        return next(matches, None)


class SimpleHeaderPaginator(BaseAPIPaginator[t.Optional[str]]):
    """Paginator class for APIs returning a pagination token in the response headers."""

    def __init__(self, key: str, *args: t.Any, **kwargs: t.Any) -> None:
        """Create a new paginator."""
        super().__init__(None, *args, **kwargs)
        self._key = key

    def get_next(self, response: Response) -> str | None:
        """Get the next page token."""
        return response.headers.get(self._key, None)


class BasePageNumberPaginator(BaseAPIPaginator[int], metaclass=ABCMeta):
    """Paginator class for APIs that use page number."""

    @abstractmethod
    def has_more(self, response: Response) -> bool:
        """Override this method to check if the endpoint has any pages left."""

    def get_next(self, response: Response) -> int | None:  # noqa: ARG002
        """Get the next page number."""
        return self._value + 1


class BaseOffsetPaginator(BaseAPIPaginator[int], metaclass=ABCMeta):
    """Paginator class for APIs that use page offset."""

    def __init__(self, start_value: int, page_size: int, *args: t.Any, **kwargs: t.Any) -> None:
        """Create a new paginator."""
        super().__init__(start_value, *args, **kwargs)
        self._page_size = page_size

    @abstractmethod
    def has_more(self, response: Response) -> bool:
        """Override this method to check if the endpoint has any pages left."""
        ...

    def get_next(self, response: Response) -> int | None:  # noqa: ARG002
        """Get the next page offset."""
        return self._value + self._page_size
