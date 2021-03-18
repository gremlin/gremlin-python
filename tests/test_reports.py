import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.reports import GremlinAPIReports, GremlinAPIReportsSecurity

from .util import mock_json, mock_data, mock_report


class TestReports(unittest.TestCase):
    @patch("requests.get")
    def test_report_attacks_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIReports.report_attacks(**mock_report), mock_data)

    @patch("requests.get")
    def test_report_clients_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIReports.report_clients(**mock_report), mock_data)

    @patch("requests.get")
    def test_report_companies_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIReports.report_companies(**mock_report), mock_data)

    @patch("requests.get")
    def test_report_pricing_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIReports.report_pricing(**mock_report), mock_data)

    @patch("requests.get")
    def test_report_teams_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIReports.report_teams(**mock_report), mock_data)

    @patch("requests.get")
    def test_report_users_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIReports.report_users(**mock_report), mock_data)

    @patch("requests.get")
    def test_report_security_access_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIReportsSecurity.report_security_access(**mock_report), mock_data
        )
