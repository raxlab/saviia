from abc import ABC, abstractmethod
from .types.http_client_types import GetArgs, UploadFileArgs


class HTTPClientContract(ABC):
    @abstractmethod
    async def get(self, args: GetArgs):
        pass

    @abstractmethod
    async def upload_file(self, args: UploadFileArgs):
        pass
