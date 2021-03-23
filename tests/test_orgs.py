import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.orgs import GremlinAPIOrgs

from .util import mock_json, mock_data, mock_identifier


class TestOrgs(unittest.TestCase):
    @patch("requests.get")
    def test_list_orgs_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIOrgs.list_orgs(), mock_data)

    @patch("requests.get")
    def test_get_org_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIOrgs.get_org(**mock_identifier), mock_data)

    @patch("requests.post")
    def test_create_org_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIOrgs.create_org(**mock_identifier), mock_data)

    @patch("requests.post")
    def test_new_certificate_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIOrgs.new_certificate(), mock_data)

    @patch("requests.delete")
    def test_delete_certificate_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIOrgs.delete_certificate(), mock_data)

    @patch("requests.delete")
    def test_delete_old_certificate_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIOrgs.delete_old_certificate(), mock_data)

    @patch("requests.post")
    def test_reset_secret_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIOrgs.reset_secret(**mock_identifier), mock_data)
