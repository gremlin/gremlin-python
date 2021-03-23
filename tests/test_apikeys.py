import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.apikeys import GremlinAPIapikeys

from .util import mock_json, mock_data


class TestAPIKeys(unittest.TestCase):
    @patch("requests.post")
    def test_create_apikey_with_decorator(self, mock_get) -> None:
        test_kwargs = {"description": "123456790", "identifier": "1234567890"}
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIapikeys.create_apikey(**test_kwargs), mock_data)

    @patch("requests.get")
    def test_list_apikeys_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIapikeys.list_apikeys(), mock_data)

    @patch("requests.delete")
    def test_revoke_apikey_with_decorator(self, mock_get) -> None:
        test_kwargs = {"description": "123456790", "identifier": "1234567890"}
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIapikeys.revoke_apikey(**test_kwargs), mock_data)
