import unittest
from unittest.mock import Mock, patch

from libs.ftp_client import FTPClient, FtpClientInitArgs


class TestFtpClientConstruct(unittest.TestCase):
    def _test_client_attributes_and_methods(
        self, mock_client, client_name, expected_properties, expected_methods
    ):
        # Arrange
        mock_client_instance = mock_client.return_value
        # Act
        client = FTPClient(
            FtpClientInitArgs(
                client_name=client_name,
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
        self.assertEqual(client.client_obj, mock_client_instance)


    @patch("libs.ftp_client.ftp_client.AioFTPClient")
    def test_should_have_expected_attributes_and_methods_for_aioftplib_client(
        self, mock_aioftp_client: Mock
    ):
        self._test_client_attributes_and_methods(
            mock_aioftp_client,
            client_name="aioftp_client",
            expected_properties=["client_name", "client_obj"],
            expected_methods=["list_files"],
        )

