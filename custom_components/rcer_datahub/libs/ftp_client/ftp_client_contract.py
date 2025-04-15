from abc import ABC, abstractmethod

from .types.ftp_client_types import ListFilesArgs, ReadFileArgs


class FTPClientContract(ABC):
    @abstractmethod
    def list_files(self, args: ListFilesArgs) -> list[str]:
        pass

    @abstractmethod
    def read_file(self, args: ReadFileArgs) -> bytes:
        pass
