import unittest
from unittest.mock import Mock, patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../../")))
from custom_components.rcer_datahub.libs.async_http_client.clients.aiohttp_client import AioHttpClient
from custom_components.rcer_datahub.libs.async_http_client.async_http_client import GetArgs, AsyncHttpClientInitArgs
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

class TestAioHttpClient(unittest.TestCase):
    def test_should_get_data_successfully(self):
        asyncio.run(self._run_test())  

    async def _run_test(self):
        # Arrange
        drive_id = "b!Row14jaFrU-1q8qzrvj3OmPPTYWXizFEpJmI-wsfH5pXxA0qQwgQS50m2xvPCZem"
        base_url = "https://graph.microsoft.com/v1.0/"
        init_args = AsyncHttpClientInitArgs(
            access_token=os.environ.get("MICROSOFT_GRAPH_ACCESS_TOKEN"),
            base_url=base_url,
        )

        async with AioHttpClient(init_args) as client:
            cloud_files = set()
            file_types = ["AVG", "EXT"]

            for file_type in file_types:
                destination_path = f"Onedrive_UC/noveno-semestre/IPRE-RCER/thies/{file_type}"
                endpoint = f"drives/{drive_id}/root:/{destination_path}:/children"
                try:
                    response = await client.get(GetArgs(endpoint=endpoint))
                    cloud_files.update({
                        f"{file_type}_{item['name']}" for item in response["value"]
                    })
                    print(response)
                except ConnectionError as e:
                    print(e)

            print(cloud_files)