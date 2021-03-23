import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.clients import GremlinAPIClients

from .util import mock_json, mock_data, mock_guid


class TestClients(unittest.TestCase):
    @patch("requests.put")
    def test_activate_client_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIClients.activate_client(**mock_guid), mock_data)

    @patch("requests.delete")
    def test_deactivate_client_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIClients.deactivate_client(**mock_guid), mock_data)

    @patch("requests.get")
    def test_list_active_clients_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIClients.list_active_clients(), mock_data)

    @patch("requests.get")
    def test_list_clients_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIClients.list_clients(), mock_data)
