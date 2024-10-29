from abc import ABC
from typing import Optional

import httpx
from typing_extensions import Self


class BaseMiddleware(ABC):
    client: httpx.AsyncClient
    next: Optional[Self]

    async def send(
        self, request: httpx.Request, transport: httpx.AsyncBaseTransport
    ) -> httpx.Response:
        if self.next:
            return await self.next.send(request, transport)
        else:
            self.client._transport = transport
            return await self.client.send(
                request,
            )


class MiddlewareManager:
    start: Optional[BaseMiddleware] = None
    current: Optional[BaseMiddleware] = None

    def add_middleware(self, middleware: BaseMiddleware) -> None:
        if self.start is None:
            self.start = middleware
            self.start.next = None
            self.current = middleware
        else:
            self.start.next = middleware
            self.current = middleware

    async def send(
        self, request: httpx.Request, transport: httpx.AsyncBaseTransport
    ) -> httpx.Response:
        if not self.current:
            raise LookupError("Please first register a middleware.")
        resp: httpx.Response = await self.current.send(request, transport)
        return resp
