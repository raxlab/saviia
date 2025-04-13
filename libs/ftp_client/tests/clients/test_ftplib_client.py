import unittest
from unittest.mock import Mock, patch
from libs.ftp_client.clients.ftplib_client import FTPLibClient, FtpClientInitArgs, ListFilesArgs


class TestFtplibClientConstruct(unittest.TestCase):
    def test_should_have_expected_attributes_and_methods_defined(self):
        # Arrange
        expected_properties = ["client"]
        expected_methods = ["list_files"]
        # Act
        client = FTPLibClient(
            FtpClientInitArgs(
                host="localhost",
                user="anonymous",
                password="12345678",
                port=21,
            )
        )
        client._close()
        # Assert
        for prop in expected_properties:
            with self.subTest(property=prop):
                self.assertTrue(hasattr(client, prop))

        for method in expected_methods:
            with self.subTest(method=method):
                self.assertTrue(
                    hasattr(client, method) and callable(getattr(client, method))
                )
        

class TestFTPLibClientListFiles(unittest.TestCase):
    @patch('libs.ftp_client.clients.ftplib_client.FTP')
    def test_should_list_files_successfully(self, mock_ftp: Mock):
        # Arrange
        mock_ftp_instance = mock_ftp.return_value
        client = FTPLibClient(
            FtpClientInitArgs(
                host="localhost",
                user="anonymous",
                password="12345678",
                port=21,
            )
        )
        expected_files = ["FILE1.BIN", "FILE2.BIN"]
        mock_ftp_instance.nlst.return_value = expected_files
        
        # Act
        files = client.list_files(ListFilesArgs(path='ftp/thies/BINFILES/'))
        # Assert
        self.assertListEqual(expected_files, files)