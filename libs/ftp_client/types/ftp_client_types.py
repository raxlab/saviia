from pydantic import BaseModel


class FtpClientInitArgs(BaseModel):
    client_name: str = "fptlib_client"
    host: str
    user: str
    password: str
    port: int = 21


class ListFilesArgs(BaseModel):
    path: str
