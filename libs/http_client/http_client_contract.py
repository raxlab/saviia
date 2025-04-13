from abc import ABC, abstractmethod
from .types.http_client_types import GetArgs, UploadFileArgs
from typing import Dict, Any

class HTTPClientContract(ABC):
    @abstractmethod
    def get(self, args: GetArgs) -> Dict[str, Any]:
        pass

    @abstractmethod
    def upload_file(self, args: UploadFileArgs) -> Dict[str, Any]:
        pass
