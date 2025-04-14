from abc import ABC, abstractmethod

from .types.ftp_client_types import ListFilesArgs, ReadFileArgs
from typing import List

class FTPClientContract(ABC):
    @abstractmethod
    def list_files(self, args: ListFilesArgs) -> List[str]:
        pass
    
    @abstractmethod
    def read_file(self, args: ReadFileArgs) -> bytes:
        pass
    
