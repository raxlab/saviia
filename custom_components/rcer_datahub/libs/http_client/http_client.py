# custom_components/data_hub/http_client.py

from .clients.request_client import RequestsClient
from .htp_client_contract import HTTPClientContract
from .types.http_client_types import GetArgs, InitArgs, UploadFileArgs


class HTTPClient(HTTPClientContract):
    CLIENTS = {"request_client": RequestsClient()}

    def __init__(self, args: InitArgs):
        if HTTPClient.CLIENTS.get(args.client_name):
            self.client_name = args.client_name
            self.client_obj = HTTPClient.CLIENTS[args.client_name]
        else:
            raise KeyError(f"Unsupported client '{args.client_name}'")

    async def get(self, args: GetArgs):
        return self.client_obj.get(args)

    async def upload_file(self, args: UploadFileArgs):
        return self.client_obj.upload_file(args)
