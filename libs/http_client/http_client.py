
from .clients.request_client import RequestsClient
from .http_client_contract import HTTPClientContract
from .types.http_client_types import GetArgs, HttpClientInitArgs, UploadFileArgs
from typing import Dict, Any

class HTTPClient(HTTPClientContract):
    CLIENTS = {"request_client"}

    def __init__(self, args: HttpClientInitArgs):
        if args.client_name not in HTTPClient.CLIENTS:
            raise KeyError(f"Unsupported client '{args.client_name}'")
        self.client_name = args.client_name

        if args.client_name == "request_client":
            self.client_obj = RequestsClient(args)

    def get(self, args: GetArgs) -> Dict[str, Any]:
        return self.client_obj.get(args)

    def upload_file(self, args: UploadFileArgs) -> Dict[str, Any]:
        return self.client_obj.upload_file(args)
