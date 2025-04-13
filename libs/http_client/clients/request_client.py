from typing import Any, Dict

import requests
from libs.http_client.http_client_contract import HTTPClientContract
from libs.http_client.types.http_client_types import GetArgs, UploadFileArgs, HttpClientInitArgs


class RequestsClient(HTTPClientContract):
    def __init__(self, args: HttpClientInitArgs):
        self.access_token = args.access_token
        self.base_url = args.base_url
        self.headers = self._build_headers()
        
    def _build_headers(self):
        return {
            'Authorization': f'Bearer {self.access_token}'
        }
        
    def get(self, args: GetArgs) -> Dict[str, Any]:
        endpoint, params = args.endpoint, args.params
        url = f'{self.base_url}/{endpoint}'
        response = requests.get(url=url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()

    def upload_file(self, args: UploadFileArgs) -> Dict[str, Any]:
        endpoint, file_bytes = args.endpoint, args.file_bytes
        url = f'{self.base_url}/{endpoint}'
        response = requests.put(url=url, headers=self.headers, data=file_bytes)
        response.raise_for_status()
        return response.json()
