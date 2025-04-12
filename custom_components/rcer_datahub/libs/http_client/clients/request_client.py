import logging
from typing import Any, Dict

import requests
from libs.http_client.htp_client_contract import HTTPClientContract
from libs.http_client.types.http_client_types import GetArgs, UploadFileArgs

_LOGGER = logging.getLogger(__name__)


class RequestsClient(HTTPClientContract):
    def get(self, args: GetArgs) -> Dict[str, Any]:
        url, params = args.url, args.params
        _LOGGER.debug(f"GET {url} | Params: {params}")
        response = requests.get(url=url, params=params)
        response.raise_for_status()
        return response.json()

    def upload_file(self, args: UploadFileArgs) -> Dict[str, Any]:
        _LOGGER.debug(f"UPLOAD FILE {args.url}")
        url, headers, file_bytes = args.url, args.headers, args.file_bytes
        response = requests.put(url=url, headers=headers, data=file_bytes)
        response.raise_for_status()
