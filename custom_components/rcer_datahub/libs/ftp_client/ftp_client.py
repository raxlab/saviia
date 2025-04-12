from .clients.aioftp_client import AioFTPClient
from .clients.ftplib_client import FTPLibClient
from .ftp_client_contract import FTPClientContract
from .types.ftp_client_types import InitArgs, ListFilesArgs

class FTPClient(FTPClientContract):
    CLIENTS = {"ftp_client", "aioftp_client"}
    def __init__(self, args: InitArgs):
        if args.client_name not in FTPClient.CLIENTS:
            raise KeyError(f"Unsupported client {args.client_name}")

        if args.client_name == "aioftp_client":
            self.client_obj = AioFTPClient(
                host=args.host, user=args.user, password=args.password, port=args.port
            )
        elif args.client_name == "ftp_client":
            self.client_obj = FTPLibClient(
                host=args.host, user=args.user, password=args.password, port=args.port
            )
        self.client_name = args.client_name

    def list_files(self, args: ListFilesArgs):
        return self.client_obj.list_files(args)
