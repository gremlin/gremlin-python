import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.providers import GremlinAPIProviders

from .util import mock_json, mock_data


class TestProviders(unittest.TestCase):
    @patch("requests.get")
    def test_list_providers_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIProviders.list_providers(), mock_data)

    @patch("requests.get")
    def test_list_aws_services_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIProviders.list_aws_services(), mock_data)
