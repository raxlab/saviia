import unittest
from unittest.mock import Mock, patch
import sys 
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../")))
from custom_components.rcer_datahub.libs.async_http_client.async_http_client import AsyncHTTPClient, AsyncHttpClientInitArgs


class TestHttpClientConstruct(unittest.TestCase):
    def _test_client_attributes_and_methods(
        self,
        mock_requests_client: Mock,
        client_name: str,
        expected_properties: list,
        expected_methods: list,
    ):
        # Arrange
        mock_client_instance = mock_requests_client.return_value
        # Act
        client = AsyncHTTPClient(
            AsyncHttpClientInitArgs(
                client_name=client_name,
                access_token="valid-access-token",
                base_url="valid-base-url",
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

    @patch("libs.async_http_client.async_http_client.AioHttpClient")
    def test_should_have_expected_attributes_and_methods_for_aiohttp_client(
        self, mock_requests_client: Mock
    ):
        self._test_client_attributes_and_methods(
            mock_requests_client,
            client_name="aiohttp_client",
            expected_properties=["client_name", "client_obj"],
            expected_methods=["get", "upload_file"],
        )
