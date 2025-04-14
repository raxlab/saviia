from abc import ABC, abstractmethod
from typing import Any, Dict

from .types.async_http_client_types import GetArgs, UploadFileArgs


class AsyncHTTPClientContract(ABC):
    @abstractmethod
    async def get(self, args: GetArgs) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def upload_file(self, args: UploadFileArgs) -> Dict[str, Any]:
        pass
