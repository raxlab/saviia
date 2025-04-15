import os

from dotenv import load_dotenv

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
from custom_components.rcer_datahub.api.types import ConfigAPI

from .utils import generate_file_content, http_response

load_dotenv()


class RCERDatahubAPI:
    PATH_AVG_FILES = "ftp/thies/BINFILES/ARCH_AV1"
    PATH_EXT_FILES = "ftp/thies/BINFILES/ARCH_EX1"
    DRIVE_ID = "b!Row14jaFrU-1q8qzrvj3OmPPTYWXizFEpJmI-wsfH5pXxA0qQwgQS50m2xvPCZem"
    FILE_TYPES = ["AVG", "EXT"]

    def __init__(self, config: ConfigAPI) -> None:
        self.async_http_client = self._initialize_http_client()
        self.ftp_client = self._initialize_ftp_client()
        self.pending = set()
        self.uploading = set()
        self.ftp_port = config.ftp_port
        self.ftp_host = config.ftp_host
        self.ftp_password = config.ftp_password
        self.ftp_user = config.ftp_user
        self.logger = config.logger

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

    def _initialize_ftp_client(self) -> FTPClient:
        """Initialize the FTP client."""
        return FTPClient(
            FtpClientInitArgs(
                client_name="aioftp_client",
                host=self.ftp_host,
                user=self.ftp_user,
                password=self.ftp_password,
                port=self.ftp_port,
            )
        )

    async def fetch_cloud_file_names(self, folder_name: str) -> set[str]:
        """Fetch file names from the RCER cloud."""
        self.logger.info("[rcer_api] fetch_cloud_file_names_started")
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
            self.logger.error("[rcer_api] fetch_cloud_file_names_error", extra={
                'error': error.__str__()
            })
        self.logger.info("[rcer_api] fetch_cloud_file_names_successful")
        return cloud_files

    async def fetch_thies_file_names(self) -> set[str]:
        """Fetch file names from the THIES FTP server."""
        self.logger.info("[rcer_api] fetch_thies_file_names_started")
        try:
            avg_files = await self.ftp_client.list_files(
                ListFilesArgs(path=self.PATH_AVG_FILES)
            )
            ext_files = await self.ftp_client.list_files(
                ListFilesArgs(path=self.PATH_EXT_FILES)
            )
            self.logger.info("[rcer_api] fetch_thies_file_names_successful")
            return {f"AVG_{name}" for name in avg_files} | {
                f"EXT_{name}" for name in ext_files
            }
        except ConnectionError as error:
            self.logger.error("[rcer_api] fetch_thies_file_names_error", extra={
                'error': error.__str__()
            })
            return set()

    async def fetch_thies_file_content(self) -> dict[str, bytes]:
        """Fetch the content of files from the THIES FTP server."""
        self.logger.info("[rcer_api] fetch_thies_file_content_started")
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
            except ConnectionError as error:
                self.logger.error("[rcer_api] fetch_thies_file_content_error", extra={
                    'message': f"Failed to fetch content for file {file}",
                    'error': error.__str__()
                })
        self.logger.info("[rcer_api] fetch_thies_file_content_successful")
        return content_files

    async def syncronize_thies_data_to_cloud(self) -> dict[str, dict[str, str]]:
        """Synchronize data from the THIES Center to the cloud."""
        self.logger.debug("[rcer_api] syncronize_thies_data_to_cloud_started")
        try:
            thies_files = await self.fetch_thies_file_names()
            cloud_files = await self.fetch_cloud_file_names(folder_name="thies")
            self.uploading = thies_files - cloud_files
            if not self.uploading:
                self.logger.info("[rcer_api] syncronize_thies_data_to_cloud_early_return", extra={
                    "message": "No new files to upload."
                })
                return http_response(message="No new files to upload.", status=204)
            thies_file_contents = await self.fetch_thies_file_content()
            data = generate_file_content(thies_file_contents)

            # TODO: Implement the logic to upload thies_file_contents to the cloud
            self.logger.info("[rcer_api] syncronize_thies_data_to_cloud_successful")
            return http_response(
                message="Uploaded data successfully",
                status=200,
                metadata=data,
            )
        except ConnectionError as error:
            error_message = "Error during upload process"
            self.logger.error("[rcer_api] syncronize_thies_data_to_cloud_error", extra={
                'message': error_message,
                'error': error.__str__()
            })
            return http_response(
                message=error_message,
                status=500,
                metadata={"error": error},
            )
