import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.halts import GremlinAPIHalts

from .util import mock_body, mock_data, mock_json


class TestHalts(unittest.TestCase):
    @patch("requests.post")
    def test_halt_all_attacks_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIHalts.halt_all_attacks(**mock_body), mock_data)
