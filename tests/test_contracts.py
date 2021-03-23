import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.contracts import GremlinAPIContracts

from .util import mock_identifier, mock_json, mock_data


class TestContracts(unittest.TestCase):
    @patch("requests.patch")
    def test_update_contract_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIContracts.update_contract(**mock_identifier), mock_data
        )
