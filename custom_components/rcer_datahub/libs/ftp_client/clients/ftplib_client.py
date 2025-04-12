from ftplib import FTP

from libs.ftp_client.ftp_client_contract import FTPClientContract
from libs.ftp_client.types.ftp_client_types import ListFilesArgs


class FTPLibClient(FTPClientContract):
    def __init__(self, host: str, user: str, password: str, port: int = 21):
        self.client = FTP(host=host, user=user, passwd=password, port=port)

    def list_files(self, args: ListFilesArgs):
        self.client.login(self.user, self.password)
        self.client.cwd(args.path)
        return self.client.nlst()
