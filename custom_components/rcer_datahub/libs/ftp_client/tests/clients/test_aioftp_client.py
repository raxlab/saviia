import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from libs.ftp_client.clients.aioftp_client import (
    AioFTPClient,
    FtpClientInitArgs,
    ListFilesArgs,
)


class TestAioFTPClientConstruct(unittest.IsolatedAsyncioTestCase):
    async def test_should_have_expected_attributes_and_methods_defined(self):
        # Arrange
        expected_properties = ["client"]
        expected_methods = ["list_files"]
        # Act
        client = AioFTPClient(
            FtpClientInitArgs(
                host="localhost",
                user="anonymous",
                password="12345678",
                port=21,
            )
        )
        # Assert
        for prop in expected_properties:
            with self.subTest(property=prop):
                self.assertTrue(hasattr(client, prop))

        for method in expected_methods:
            with self.subTest(method=method):
                self.assertTrue(
                    hasattr(client, method) and callable(getattr(client, method))
                )


class TestAioFTPClientListFiles(unittest.IsolatedAsyncioTestCase):
    @patch("libs.ftp_client.clients.aioftp_client.Client")
    async def test_should_list_files_successfully(self, mock_aioftp_client):
        # Arrange
        mock_client_instance = mock_aioftp_client.return_value
        mock_client_instance.connect = AsyncMock()
        mock_client_instance.login = AsyncMock()
        expected_files = ["FILE1.BIN", "FILE2.BIN"]
        mock_list_response = [
            (SimpleNamespace(name=name), None) for name in expected_files
        ]
        mock_client_instance.list.return_value.__aiter__.return_value = (
            mock_list_response
        )
        client = AioFTPClient(
            FtpClientInitArgs(
                host="localhost",
                user="anonymous",
                password="12345678",
                port=21,
            )
        )
        path = "ftp/thies/BINFILES/"
        # Act
        files = await client.list_files(ListFilesArgs(path=path))
        # Assert
        self.assertListEqual(expected_files, files)
