import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.metadata import GremlinAPIMetadata

from .util import mock_json, mock_data


class TestMetadata(unittest.TestCase):
    @patch("requests.get")
    def test_get_metadata_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIMetadata.get_metadata(), mock_data)
