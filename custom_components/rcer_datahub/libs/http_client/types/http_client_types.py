from pydantic import BaseModel, Field


class InitArgs(BaseModel):
    client_name: str = "request_client"


class GetArgs(BaseModel):
    url: str
    params: dict = Field(default_factory=dict())


class UploadFileArgs(BaseModel):
    url: str
    headers: str
    file_bytes: bytes
