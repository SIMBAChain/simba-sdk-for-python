from types import TracebackType
from typing import Dict, List, Optional

import httpx
from httpx import Response
from httpx._types import RequestFiles
from pydantic_core import Url
from typing_extensions import Type

from simba_sdk import config
from simba_sdk.config import settings
from simba_sdk.core.requests.auth.token_store import BaseTokenStore
from simba_sdk.core.requests.exception import RequestException
from simba_sdk.core.requests.middleware.manager import MiddlewareManager


class Client:
    def __init__(
        self,
        base_url: str,
        headers: Dict[str, str] = {},
        cookies: Dict[str, str] = {},
        client: Optional[httpx.AsyncClient] = None,
        timeout: Optional[float] = 100.0,
        token_store: Optional[BaseTokenStore] = None,
        middleware: Optional[List[str]] = None,
    ):
        Url(base_url)
        self._base_url = base_url
        self._client: httpx.AsyncClient = (
            httpx.AsyncClient(headers=headers, cookies=cookies, timeout=timeout)
            if not client
            else client
        )
        self.token_store = token_store

        self.middleware_manager = MiddlewareManager()
        if middleware is not None:
            for ware in middleware:
                middleware_instance = config.MIDDLEWARE[ware]()
                middleware_instance.client = self._client
                self.middleware_manager.add_middleware(middleware_instance)
        else:
            for ware in config.MIDDLEWARE.keys():
                middleware_instance = config.MIDDLEWARE[ware]()
                middleware_instance.client = self._client
                self.middleware_manager.add_middleware(middleware_instance)

    async def __aenter__(self) -> "Client":
        await self._client.__aenter__()  # type: ignore
        return self

    async def __aexit__(
        self,
        exc_type: Type[Exception],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        await self._client.__aexit__(exc_type, exc_val, exc_tb)  # type: ignore

    def build_url(self, url: str) -> str:
        if not url.startswith("/"):
            url = "/" + url

        return self._base_url + url

    def _get_token(self) -> Optional[str]:
        if self.token_store:
            token: Optional[str] = self.token_store.get_token(settings.CLIENT_ID)
            return token
        raise LookupError("No token_path store registered to this client")

    async def get(
        self,
        url: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        cookies: Optional[Dict] = None,
    ) -> Response:
        return await self.send(
            "GET", url, params=params, headers=headers, cookies=cookies
        )

    async def post(
        self,
        url: str,
        data: Optional[Dict[str, str]] = None,
        upload_file: Optional[RequestFiles] = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        cookies: Optional[Dict] = None,
    ) -> Response:
        if not upload_file and not data:
            raise RequestException(
                status_code=400,
                message="Post requests must either send an upload_file or data.",
            )
        return await self.send(
            "POST",
            url,
            data=data,
            upload_file=upload_file,
            params=params,
            headers=headers,
            cookies=cookies,
        )

    async def put(
        self,
        url: str,
        data: Optional[Dict[str, str]] = None,
        upload_file: Optional[RequestFiles] = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        cookies: Optional[Dict] = None,
    ) -> Response:
        return await self.send(
            "PUT",
            url,
            data=data,
            upload_file=upload_file,
            params=params,
            headers=headers,
            cookies=cookies,
        )

    async def patch(
        self,
        url: str,
        data: Optional[Dict[str, str]] = None,
        upload_file: Optional[RequestFiles] = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        cookies: Optional[Dict] = None,
    ) -> Response:
        return await self.send(
            "PATCH",
            url,
            data=data,
            upload_file=upload_file,
            params=params,
            headers=headers,
            cookies=cookies,
        )

    async def delete(
        self,
        url: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        cookies: Optional[Dict] = None,
    ) -> Response:
        return await self.send(
            "DELETE", url, params=params, headers=headers, cookies=cookies
        )

    async def send(
        self,
        method: str,
        url: str,
        data: Optional[Dict] = None,
        upload_file: Optional[RequestFiles] = None,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None,
        cookies: Optional[Dict] = None,
    ) -> Response:
        """
        Send a request via the MiddlewareManager
        """
        if data is None:
            data = {}
        if cookies is None:
            cookies = {}
        if headers is None:
            headers = {}
        if params is None:
            params = {}

        token = self._get_token()
        if token:
            headers = {"Authorization": f"Bearer {token}"}

        request = self._client.build_request(
            method,
            self.build_url(url),
            data=data,
            files=upload_file,
            params=params,
            headers=headers,
            cookies=cookies,
        )
        resp: Response = await self.middleware_manager.send(
            request, self._client._transport
        )
        if resp.status_code >= 300:
            try:
                error = resp.json()["detail"]
            except (KeyError, AttributeError):
                error = resp.text
            raise RequestException(
                status_code=resp.status_code,
                message=f"Request was unsuccessful: {error}",
            )
        return resp

    async def authorise(self, token_url: str, headers: Optional[Dict] = None) -> None:
        """
        Get an auth token_path via client credentials and store
        """
        if headers is None:
            headers = {}
        request = self._client.build_request(
            "POST",
            token_url,
            data={
                "grant_type": "client_credentials",
                "client_id": settings.CLIENT_ID,
                "client_secret": settings.CLIENT_SECRET,
            },
            headers=headers,
        )
        resp: Response = await self.middleware_manager.send(
            request, self._client._transport
        )
        if not resp.status_code == 200:
            raise RequestException(
                status_code=resp.status_code,
                message=f"Authorization failed: {resp.text}",
            )
        if not self.token_store:
            raise LookupError("No token_path store registered to this client")
        self.token_store.set_token(
            identifier=settings.CLIENT_ID,
            token=resp.json()["access_token"],
            expires=resp.json()["expires_at"],
        )
