from typing import Any, Dict

from .clients.aiohttp_client import AioHttpClient
from .http_client_contract import HTTPClientContract
from .types.http_client_types import GetArgs, HttpClientInitArgs, UploadFileArgs


class HTTPClient(HTTPClientContract):
    CLIENTS = {"aiohttp_client"}

    def __init__(self, args: HttpClientInitArgs):
        if args.client_name not in HTTPClient.CLIENTS:
            raise KeyError(f"Unsupported client '{args.client_name}'")
        self.client_name = args.client_name

        if args.client_name == "aiohttp_client":
            self.client_obj = AioHttpClient(args)

    async def get(self, args: GetArgs) -> Dict[str, Any]:
        return await self.client_obj.get(args)

    async def upload_file(self, args: UploadFileArgs) -> Dict[str, Any]:
        return await self.client_obj.upload_file(args)
