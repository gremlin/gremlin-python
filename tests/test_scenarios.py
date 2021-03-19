import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.scenarios import GremlinAPIScenarios, GremlinAPIScenariosRecommended

from .util import mock_json, mock_data, mock_scenario, mock_payload, mock_scenario_guid


class TestScenarios(unittest.TestCase):
    def test__error_if_not_scenario_body(self) -> None:
        test_output = GremlinAPIScenarios._error_if_not_scenario_body(**mock_payload)
        self.assertEqual(test_output, str(mock_data))

    @patch("requests.get")
    def test_list_scenarios_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIScenarios.list_scenarios(), mock_data)

    @patch("requests.post")
    def test_create_scenario_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIScenarios.create_scenario(**mock_payload), mock_data)

    @patch("requests.get")
    def test_get_scenario_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIScenarios.get_scenario(**mock_scenario_guid), mock_data
        )

    @patch("requests.put")
    def test_update_scenario_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIScenarios.update_scenario(**mock_scenario_guid), mock_data
        )

    @patch("requests.post")
    def test_archive_scenario_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIScenarios.archive_scenario(**mock_scenario_guid), mock_data
        )

    @patch("requests.post")
    def test_restore_scenario_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIScenarios.restore_scenario(**mock_scenario_guid), mock_data
        )

    @patch("requests.get")
    def test_list_scenario_runs_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIScenarios.list_scenario_runs(**mock_scenario_guid), mock_data
        )

    @patch("requests.post")
    def test_run_scenario_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIScenarios.run_scenario(**mock_scenario_guid), mock_data
        )

    @patch("requests.get")
    def test_get_scenario_run_details_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIScenarios.get_scenario_run_details(**mock_scenario_guid),
            mock_data,
        )

    @patch("requests.put")
    def test_update_scenario_result_flags_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIScenarios.update_scenario_result_flags(**mock_scenario_guid),
            mock_data,
        )

    @patch("requests.put")
    def test_update_scenario_result_notes_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIScenarios.update_scenario_result_notes(**mock_scenario_guid),
            mock_data,
        )

    @patch("requests.get")
    def test_list_scenario_schedules_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIScenarios.list_scenario_schedules(**mock_scenario_guid), mock_data
        )

    @patch("requests.get")
    def test_list_active_scenarios_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIScenarios.list_active_scenarios(**mock_scenario_guid), mock_data
        )

    @patch("requests.get")
    def test_list_archived_scenarios_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIScenarios.list_archived_scenarios(**mock_scenario_guid), mock_data
        )

    @patch("requests.get")
    def test_list_draft_scenarios_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIScenarios.list_draft_scenarios(**mock_scenario_guid), mock_data
        )

    @patch("requests.post")
    def test_halt_scenario_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIScenarios.halt_scenario(**mock_scenario_guid), mock_data
        )

    @patch("requests.get")
    def test_list_recommended_scenarios_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIScenariosRecommended.list_recommended_scenarios(
                **mock_scenario_guid
            ),
            mock_data,
        )

    @patch("requests.get")
    def test_get_recommended_scenario_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIScenariosRecommended.get_recommended_scenario(
                **mock_scenario_guid
            ),
            mock_data,
        )

    @patch("requests.get")
    def test_get_recommended_scenario_static_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(
            GremlinAPIScenariosRecommended.get_recommended_scenario_static(
                **mock_scenario_guid
            ),
            mock_data,
        )
