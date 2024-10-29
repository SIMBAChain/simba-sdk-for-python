import re

import httpx

from simba_sdk.core.requests.middleware.manager import BaseMiddleware


class UrlAppendTrailingSlashHandler(BaseMiddleware):
    def __init__(self) -> None:
        """Create an instance of UrlReplaceHandler

        Args:
            options to pass to the handler.
            Defaults to UrlReplaceHandlerOption
        """
        super().__init__()

    async def send(
        self,
        request: httpx.Request,
        transport: httpx.AsyncBaseTransport,
    ) -> httpx.Response:  # type: ignore
        """To execute the current middleware

        Args:
            request (httpx.Request): The prepared request object
            transport(httpx.AsyncBaseTransport): The HTTP transport to use

        Returns:
            Response: The response object.
        """
        if request.method == "GET":
            if request.url.path[-1] != "/":
                url_string: str = self.append_trailing_slash(str(request.url))
                request.url = httpx.URL(url_string)
        response: httpx.Response = await super().send(request, transport)
        return response

    @staticmethod
    def append_trailing_slash(url_str: str) -> str:
        # match groups - 1: resource path, 2: query string
        url_pattern = r"^(https?://[A-z-.]+(?:/[A-z]+))(\?.*)?$"
        # insert a '/' after the resource path
        url_replacement = r"\1/\2"
        url_str = re.sub(url_pattern, url_replacement, url_str)
        return url_str
