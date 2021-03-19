import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.templates import GremlinAPITemplates

from .util import mock_json, mock_data, mock_body, mock_guid


class TestTemplates(unittest.TestCase):
    @patch("requests.get")
    def test_list_templates_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPITemplates.list_templates(), mock_data)

    @patch("requests.post")
    def test_create_template_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPITemplates.create_template(**mock_body), mock_data)

    @patch("requests.get")
    def test_get_template_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPITemplates.get_template(**mock_guid), mock_data)

    @patch("requests.delete")
    def test_delete_template_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPITemplates.delete_template(**mock_guid), mock_data)

    @patch("requests.get")
    def test_list_command_templates_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPITemplates.list_command_templates(), mock_data)

    @patch("requests.get")
    def test_list_target_templates_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPITemplates.list_target_templates(), mock_data)

    @patch("requests.get")
    def test_list_trigger_templates_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPITemplates.list_trigger_templates(), mock_data)
