from .clients.aioftp_client import AioFTPClient
from .ftp_client_contract import FTPClientContract
from .types.ftp_client_types import FtpClientInitArgs, ListFilesArgs, ReadFileArgs


class FTPClient(FTPClientContract):
    CLIENTS = {"aioftp_client"}

    def __init__(self, args: FtpClientInitArgs) -> None:
        if args.client_name not in FTPClient.CLIENTS:
            msg = f"Unsupported client {args.client_name}"
            raise KeyError(msg)

        if args.client_name == "aioftp_client":
            self.client_obj = AioFTPClient(args)
        self.client_name = args.client_name

    def list_files(self, args: ListFilesArgs) -> list[str]:
        return self.client_obj.list_files(args)

    def read_file(self, args: ReadFileArgs) -> bytes:
        return self.client_obj.read_file(args)
