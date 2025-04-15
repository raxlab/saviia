from abc import ABC, abstractmethod
from typing import Any

from .types.async_http_client_types import GetArgs, UploadFileArgs


class AsyncHTTPClientContract(ABC):
    """
    A contract for asynchronous HTTP client implementations.

    This abstract base class defines the required methods for performing
    HTTP GET requests and uploading files asynchronously.

    Methods.
    -------
    get(args: GetArgs) -> dict[str, Any]
        Perform an HTTP GET request with the specified arguments.

    upload_file(args: UploadFileArgs) -> dict[str, Any]
        Upload a file using the specified arguments.
    """

    @abstractmethod
    async def get(self, args: GetArgs) -> dict[str, Any]:
        pass

    @abstractmethod
    async def upload_file(self, args: UploadFileArgs) -> dict[str, Any]:
        pass
