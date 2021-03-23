import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.saml import GremlinAPISaml

from .util import mock_json, mock_data, mock_saml


class TestSaml(unittest.TestCase):
    @patch("requests.post")
    def test_acs_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPISaml.acs(**mock_saml), mock_get.return_value)

    @patch("requests.get")
    def test_samllogin_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPISaml.samllogin(**mock_saml), mock_data)

    @patch("requests.get")
    def test_metadata_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPISaml.metadata(), mock_data)

    @patch("requests.post")
    def test_sessions_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPISaml.sessions(**mock_saml), mock_data)
