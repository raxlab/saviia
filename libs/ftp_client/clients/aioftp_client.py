from typing import List

from aioftp import Client

from libs.ftp_client.ftp_client_contract import FTPClientContract
from libs.ftp_client.types.ftp_client_types import FtpClientInitArgs, ListFilesArgs


class AioFTPClient(FTPClientContract):
    def __init__(self, args: FtpClientInitArgs):
        self.host = args.host
        self.port = args.port
        self.password = args.password
        self.user = args.user
        self.client = Client()

    async def _async_start(self) -> None:
        await self.client.connect(host=self.host, port=self.port)
        await self.client.login(user=self.user, password=self.password)

    async def list_files(self, args: ListFilesArgs) -> List[str]:
        await self._async_start()
        return [
            path.name async for path, _ in self.client.list(args.path, recursive=False)
        ]
