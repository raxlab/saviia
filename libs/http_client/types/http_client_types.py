from pydantic import BaseModel, Field


class HttpClientInitArgs(BaseModel):
    access_token: str
    base_url: str
    client_name: str = "aiohttp_client"


class GetArgs(BaseModel):
    endpoint: str
    params: dict | None = Field(default=None)


class UploadFileArgs(BaseModel):
    endpoint: str
    file_bytes: bytes
