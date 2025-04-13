from ...libs.ftp_client import FTPClient, ListFilesArgs, FtpClientInitArgs
from ...libs.http_client import HTTPClient, GetArgs
from .const import LOGGER

class DataHubRemoteManager:
    PATH_AVG_FILES = "ftp/thies/BINFILES/ARCH_AV1"
    PATH_EXT_FILES = "ftp/thies/BINFILES/ARCH_AV1"

    def __init__(self, http_client: HTTPClient):
        self.http_client = http_client
        self.pending = set()
        self.uploading = set()

    def extract_cloud_data(self, folder_name: str) -> set:
        drive_id = "b!Row14jaFrU-1q8qzrvj3OmPPTYWXizFEpJmI-wsfH5pXxA0qQwgQS50m2xvPCZem"

        cloud_files = set()
        file_types = ["AVG", "EXT"]
        try: 
            for file_type in file_types:
                destination_path = (
                    f"Onedrive_UC/noveno-semestre/IPRE-RCER/{folder_name}/{file_type}"
                )
                endpoint = f"drives/{drive_id}/root:/{destination_path}:/children"
                response = self.http_client.get(GetArgs(endpoint=endpoint))
                cloud_files.update(
                    {f"{file_type}_{item['name']}" for item in response["value"]}
                )
            return cloud_files
        except ConnectionError as error:
            LOGGER.error(f"Unexpected error occurred while extracting RCER Cloud Data: {error}")
            

    async def extract_thies_data(self) -> set:
        ftp_client = FTPClient(
            FtpClientInitArgs(
                client_name="aioftp_client",
                host="localhost",
                user="anonymous",
                password="12345678",
                port=21,
            )
        )
        average_files = set(
            f"AVG_{name}"
            for name in await ftp_client.list_files(
                ListFilesArgs(path=DataHubRemoteManager.PATH_AVG_FILES)
            )
        )
        extreme_files = set(
            f"EXT_{name}"
            for name in await ftp_client.list_files(
                ListFilesArgs(path=DataHubRemoteManager.PATH_EXT_FILES)
            )
        )
        return average_files | extreme_files

    async def verify_pending_files(self) -> None:
        # TODO: Make the logic code for pending files
        return None

    async def upload_data(self):
        """Extracting data from THIES Center"""
        thies_data = await self.extract_thies_data()
        cloud_data = await self.extract_cloud_data("thies")
        data_to_upload = thies_data.difference(cloud_data)

        return None

    async def extract_manual(self):
        return None
