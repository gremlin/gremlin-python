import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.reports import GremlinAPIReports, GremlinAPIReportsSecurity

from .util import (
    mock_json,
    mock_data,
    mock_paged_json,
    mock_paged_data,
    mock_paged_json_page1,
    mock_paged_json_page2,
    mock_report,
)


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
        mock_get.return_value.json = mock_paged_json
        self.assertEqual(GremlinAPIReports.report_teams(**mock_report), [mock_data])

    @patch("requests.get")
    def test_report_teams_pagination(self, mock_get) -> None:
        page1 = requests.Response()
        page1.status_code = 200
        page1.json = mock_paged_json_page1
        page2 = requests.Response()
        page2.status_code = 200
        page2.json = mock_paged_json_page2
        mock_get.side_effect = [page1, page2]
        result = GremlinAPIReports.report_teams(**mock_report)
        self.assertEqual(len(result), 2)
        self.assertEqual(mock_get.call_count, 2)
        second_call_url = mock_get.call_args_list[1][0][0]
        self.assertIn("pageToken=next-page-token", second_call_url)

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
