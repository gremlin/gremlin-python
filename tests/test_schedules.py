import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.schedules import GremlinAPISchedules

from .util import mock_json, mock_data, mock_body, mock_guid, mock_scenario_guid


class TestSchedules(unittest.TestCase):
    @patch("requests.post")
    def test_create_schedule_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPISchedules.create_schedule(**mock_body), mock_data)

    @patch("requests.get")
    def test_get_schedule_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPISchedules.get_schedule(**mock_guid), mock_data)

    @patch("requests.delete")
    def test_delete_schedule_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPISchedules.delete_schedule(**mock_guid), mock_data)

    @patch("requests.get")
    def test_list_active_schedules_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPISchedules.list_active_schedules(), mock_data)

    @patch("requests.get")
    def test_list_attack_schedules_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPISchedules.list_attack_schedules(), mock_data)

    @patch("requests.post")
    def test_create_attack_schedule_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPISchedules.create_attack_schedule(**mock_body), mock_data
        )

    @patch("requests.get")
    def test_get_attack_schedule_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPISchedules.get_attack_schedule(**mock_guid), mock_data
        )

    @patch("requests.delete")
    def test_delete_attack_schedule_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPISchedules.delete_attack_schedule(**mock_guid), mock_data
        )

    @patch("requests.get")
    def test_list_scenario_schedules_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPISchedules.list_scenario_schedules(), mock_data)

    @patch("requests.post")
    def test_create_scenario_schedule_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPISchedules.create_scenario_schedule(**mock_body), mock_data
        )

    @patch("requests.get")
    def test_get_scenario_schedule_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPISchedules.get_scenario_schedule(**mock_guid), mock_data
        )

    @patch("requests.post")
    def test_update_scenario_schedule_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPISchedules.update_scenario_schedule(**mock_scenario_guid),
            mock_data,
        )

    @patch("requests.delete")
    def test_delete_scenario_schedule_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPISchedules.delete_scenario_schedule(**mock_guid), mock_data
        )

    @patch("requests.post")
    def test_enable_scenario_schedule_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPISchedules.enable_scenario_schedule(**mock_guid), mock_data
        )

    @patch("requests.delete")
    def test_disable_scenario_schedule_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPISchedules.disable_scenario_schedule(**mock_guid), mock_data
        )
