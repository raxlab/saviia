from aioftp import Client
from libs.ftp_client.ftp_client_contract import FTPClientContract
from libs.ftp_client.types.ftp_client_types import ListFilesArgs


class AioFTPClient(FTPClientContract):
    def __init__(self, host, user, password, port):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.client = Client.context(self.host, self.user, self.password, self.port)

    async def list_files(self, args: ListFilesArgs):
        await self.client.change_directory(args.path)
        files = [path.name async for path in self.client.list()]
        return files
