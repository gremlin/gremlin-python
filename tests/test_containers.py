import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.containers import GremlinAPIContainers

from .util import mock_json, mock_data


class TestContainers(unittest.TestCase):
    @patch("requests.get")
    def test_list_containers_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIContainers.list_containers(), mock_data)
