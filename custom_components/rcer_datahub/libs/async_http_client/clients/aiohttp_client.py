from typing import Any

from aiohttp import ClientError, ClientSession

from custom_components.rcer_datahub.libs.async_http_client.async_http_client_contract import (
    AsyncHTTPClientContract,
)
from custom_components.rcer_datahub.libs.async_http_client.types.async_http_client_types import (
    AsyncHttpClientInitArgs,
    GetArgs,
    UploadFileArgs,
)


class AioHttpClient(AsyncHTTPClientContract):
    def __init__(self, args: AsyncHttpClientInitArgs) -> None:
        self.access_token = args.access_token
        self.base_url = args.base_url
        self.headers = self._build_headers()
        self.session: ClientSession | None = None

    def _build_headers(self) -> dict:
        return {"Authorization": f"Bearer {self.access_token}"}

    async def __aenter__(self) -> "AioHttpClient":
        self.session = ClientSession(headers=self.headers, base_url=self.base_url)
        return self

    async def __aexit__(
        self, _exc_type: type[BaseException], _exc_val: BaseException, _exc_tb: Any
    ) -> None:
        await self.session.close()

    async def get(self, args: GetArgs) -> dict[str, Any]:
        try:
            endpoint, params = args.endpoint.lstrip("/"), args.params
            response = await self.session.get(endpoint, params=params)
            response.raise_for_status()
            return await response.json()
        except ClientError as error:
            raise ConnectionError(error) from error

    async def upload_file(self, args: UploadFileArgs) -> dict[str, Any]:
        try:
            endpoint, file_bytes = args.endpoint.lstrip("/"), args.file_bytes
            response = await self.session.put(endpoint, data=file_bytes)
            response.raise_for_status()
            return await response.json()
        except ClientError as error:
            raise ConnectionError(error) from error
