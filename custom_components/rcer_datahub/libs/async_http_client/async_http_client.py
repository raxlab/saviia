from typing import Any

from .async_http_client_contract import AsyncHTTPClientContract
from .clients.aiohttp_client import AioHttpClient
from .types.async_http_client_types import (
    AsyncHttpClientInitArgs,
    GetArgs,
    UploadFileArgs,
)


class AsyncHTTPClient(AsyncHTTPClientContract):
    CLIENTS = {"aiohttp_client"}

    def __init__(self, args: AsyncHttpClientInitArgs) -> None:
        if args.client_name not in AsyncHTTPClient.CLIENTS:
            msg = f"Unsupported client '{args.client_name}'"
            raise KeyError(msg)
        self.client_name = args.client_name

        if args.client_name == "aiohttp_client":
            self.client_obj = AioHttpClient(args)

    async def __aenter__(self):
        return await self.client_obj.__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client_obj.__aexit__(exc_type, exc_val, exc_tb)

    async def get(self, args: GetArgs) -> dict[str, Any]:
        return await self.client_obj.get(args)

    async def upload_file(self, args: UploadFileArgs) -> dict[str, Any]:
        return await self.client_obj.upload_file(args)
