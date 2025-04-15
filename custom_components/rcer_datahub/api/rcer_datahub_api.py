import os
from http import HTTPStatus
from typing import Dict, Set

from dotenv import load_dotenv

from custom_components.rcer_datahub.const import LOGGER
from custom_components.rcer_datahub.libs.async_http_client import (
    AsyncHTTPClient,
    AsyncHttpClientInitArgs,
    GetArgs,
)
from custom_components.rcer_datahub.libs.ftp_client import (
    FTPClient,
    FtpClientInitArgs,
    ListFilesArgs,
    ReadFileArgs,
)

from .utils import generate_file_content, http_response

load_dotenv()


class RCERDatahubAPI:
    PATH_AVG_FILES = "ftp/thies/BINFILES/ARCH_AV1"
    PATH_EXT_FILES = "ftp/thies/BINFILES/ARCH_EX1"
    DRIVE_ID = "b!Row14jaFrU-1q8qzrvj3OmPPTYWXizFEpJmI-wsfH5pXxA0qQwgQS50m2xvPCZem"
    FILE_TYPES = ["AVG", "EXT"]

    def __init__(self):
        self.async_http_client = self._initialize_http_client()
        self.ftp_client = self._initialize_ftp_client()
        self.pending = set()
        self.uploading = set()

    @staticmethod
    def _initialize_http_client() -> AsyncHTTPClient:
        """Initialize the HTTP client."""
        return AsyncHTTPClient(
            AsyncHttpClientInitArgs(
                client_name="aiohttp_client",
                access_token=os.getenv("MICROSOFT_GRAPH_ACCESS_TOKEN"),
                base_url="https://graph.microsoft.com/v1.0/",
            )
        )

    @staticmethod
    def _initialize_ftp_client() -> FTPClient:
        """Initialize the FTP client."""
        return FTPClient(
            FtpClientInitArgs(
                client_name="aioftp_client",
                host="localhost",
                user="anonymous",
                password="12345678",
                port=21,
            )
        )

    async def fetch_cloud_file_names(self, folder_name: str) -> Set[str]:
        """Fetch file names from the RCER cloud."""
        cloud_files = set()
        try:
            async with self.async_http_client:
                for file_type in self.FILE_TYPES:
                    destination_path = f"Onedrive_UC/noveno-semestre/IPRE-RCER/{folder_name}/{file_type}"
                    endpoint = (
                        f"drives/{self.DRIVE_ID}/root:/{destination_path}:/children"
                    )
                    response = await self.async_http_client.get(
                        GetArgs(endpoint=endpoint)
                    )
                    cloud_files.update(
                        {f"{file_type}_{item['name']}" for item in response["value"]}
                    )
        except ConnectionError as error:
            LOGGER.error(f"Error fetching cloud file names: {error}")
        return cloud_files

    async def fetch_thies_file_names(self) -> Set[str]:
        """Fetch file names from the THIES FTP server."""
        try:
            avg_files = await self.ftp_client.list_files(
                ListFilesArgs(path=self.PATH_AVG_FILES)
            )
            ext_files = await self.ftp_client.list_files(
                ListFilesArgs(path=self.PATH_EXT_FILES)
            )
            return {f"AVG_{name}" for name in avg_files} | {
                f"EXT_{name}" for name in ext_files
            }
        except Exception as error:
            LOGGER.error(f"Error fetching THIES file names: {error}")
            return set()

    async def fetch_thies_file_content(self) -> Dict[str, bytes]:
        """Fetch the content of files from the THIES FTP server."""
        content_files = {}
        for file in self.uploading:
            try:
                origin, filename = file.split("_", 1)
                file_path = (
                    f"{self.PATH_AVG_FILES}/{filename}"
                    if origin == "AVG"
                    else f"{self.PATH_EXT_FILES}/{filename}"
                )
                content = await self.ftp_client.read_file(ReadFileArgs(file_path))
                content_files[filename] = content
            except Exception as error:
                LOGGER.error(f"Failed to fetch content for file {file}: {error}")
        return content_files

    async def syncronize_thies_data_to_cloud(self) -> Dict[str, Dict[str, str]]:
        """Synchronize data from the THIES Center to the cloud."""
        try:
            thies_files = await self.fetch_thies_file_names()
            cloud_files = await self.fetch_cloud_file_names(folder_name="thies")
            self.uploading = thies_files - cloud_files
            if not self.uploading:
                LOGGER.info("No new files to upload.")
                return {"status": 200, "message": "No new files to upload."}
            thies_file_contents = await self.fetch_thies_file_content()
            data = generate_file_content(thies_file_contents)

            # TODO: Implement the logic to upload thies_file_contents to the cloud

            return http_response(
                message="Uploaded data successfully!",
                status=HTTPStatus.OK,
                metadata=data,
            )
        except ConnectionError as error:
            error_message = "Error during upload process"
            LOGGER.error(f"{error_message}: {error}")
            return http_response(
                message=error_message,
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
                metadata={"error": error},
            )

    async def verify_pending_files(self) -> None:
        """Verify pending files (to be implemented)."""
        # TODO: Implement logic for verifying pending files
        pass

    async def extract_manual(self):
        """Placeholder for manual extraction logic."""
        return None
