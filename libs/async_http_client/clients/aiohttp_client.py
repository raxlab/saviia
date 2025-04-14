from typing import Any, Dict

from aiohttp import ClientError, ClientSession

from libs.async_http_client.async_http_client_contract import AsyncHTTPClientContract
from libs.async_http_client.types.async_http_client_types import (
    GetArgs,
    AsyncHttpClientInitArgs,
    UploadFileArgs,
)


class AioHttpClient(AsyncHTTPClientContract):
    def __init__(self, args: AsyncHttpClientInitArgs):
        self.access_token = args.access_token
        self.base_url = args.base_url
        self.headers = self._build_headers()
        self.session: ClientSession | None = None

    def _build_headers(self):
        return {"Authorization": f"Bearer {self.access_token}"}

    async def __aenter__(self):
        self.session = ClientSession(headers=self.headers, base_url=self.base_url)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def get(self, args: GetArgs) -> Dict[str, Any]:
        try:
            endpoint, params = args.endpoint.lstrip("/"), args.params
            response = await self.session.get(endpoint, params=params)
            response.raise_for_status()
            return await response.json()
        except ClientError as error:
            raise ConnectionError(error)

    async def upload_file(self, args: UploadFileArgs) -> Dict[str, Any]:
        try:
            endpoint, file_bytes = args.endpoint.lstrip("/"), args.file_bytes
            response = await self.session.put(endpoint, data=file_bytes)
            response.raise_for_status()
            return await response.json()
        except ClientError as error:
            raise ConnectionError(error)
