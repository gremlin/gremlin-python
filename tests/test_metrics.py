import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.metrics import GremlinAPIMetrics

from .util import mock_json, mock_data, mock_metrics


class TestMetrics(unittest.TestCase):
    @patch("requests.get")
    def test_get_attack_metrics_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIMetrics.get_attack_metrics(**mock_metrics), mock_data
        )

    @patch("requests.get")
    def test_get_scenario_run_metrics_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIMetrics.get_scenario_run_metrics(**mock_metrics), mock_data
        )
