import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.attack_helpers import (
    GremlinAttackTargetHelper,
    GremlinTargetHosts,
    GremlinTargetContainers,
    GremlinAttackCommandHelper,
    GremlinNetworkAttackHelper,
)

from .util import mock_data

attack_helper_params_custom = {
    "strategy_type": "Exact",
    "exact": 1,
    # "percent": 10,
}

attack_helper_params_default = {
    "strategy_type": "Random",
    # "exact": 1,
    "percent": 10,
}


class TestAttackHelpers(unittest.TestCase):
    def test_target_helper_target_definition(self) -> None:
        helper = GremlinAttackTargetHelper(**attack_helper_params_custom)
        test_output = helper.target_definition()
        expected_output = {
            "strategyType": attack_helper_params_custom["strategy_type"],
            "strategy": {"count": str(attack_helper_params_custom["exact"])},
        }
        self.assertEqual(test_output, expected_output)

        helper = GremlinAttackTargetHelper()
        test_output = helper.target_definition()
        expected_output = {
            "strategyType": attack_helper_params_default["strategy_type"],
            "strategy": {"percentage": attack_helper_params_default["percent"]},
        }
        self.assertEqual(test_output, expected_output)

    def test_target_helper_target_definition_graph(self) -> None:
        helper = GremlinAttackTargetHelper(**attack_helper_params_custom)
        test_output = helper.target_definition_graph()
        expected_output = {
            "strategy_type": attack_helper_params_custom["strategy_type"],
            "strategy": {
                "count": str(attack_helper_params_custom["exact"]),
                "type": attack_helper_params_custom["strategy_type"],
            },
        }
        self.assertEqual(test_output, expected_output)

        helper = GremlinAttackTargetHelper()
        test_output = helper.target_definition_graph()
        expected_output = {
            "strategy_type": attack_helper_params_default["strategy_type"],
            "strategy": {
                "percentage": attack_helper_params_default["percent"],
                "type": "RandomPercent",
            },
        }
        self.assertEqual(test_output, expected_output)

    @patch("requests.get")
    def test_filter_active_tags_with_decorator(self, mock_get) -> None:
        expected_output = {
            "os-type": [None],
            "os-version": [None, "test10"],
            "os_type": ["testwindows"],
        }

        def mock_json():
            return [{"tags": {"os_type": "testwindows", "os-version": "test10"}}]

        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        helper = GremlinTargetHosts()
        helper._filter_active_tags()
        self.assertEqual(helper._active_tags, expected_output)

    @patch("requests.get")
    def test_filter_active_labels_with_decorator(self, mock_get) -> None:
        expected_output = {"os_type": ["testwindows"], "os-version": ["test10"]}

        def mock_json():
            return [
                {"container_labels": {"os_type": "testwindows", "os-version": "test10"}}
            ]

        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        helper = GremlinTargetContainers()
        helper._filter_active_labels()
        self.assertEqual(helper._active_labels, expected_output)

    def test_impact_definition(self) -> None:
        expected_output = {
            "commandArgs": {"cliArgs": ["memory", "-l", "100"], "length": 100},
            "commandType": "memory",
        }

        helper = GremlinAttackCommandHelper()
        helper.shortType = expected_output["commandType"]
        helper.length = expected_output["commandArgs"]["length"]

        helper_output = helper.impact_definition()
        self.assertEqual(helper_output, expected_output)

    def test_impact_definition_graph(self) -> None:
        expected_output = {
            "infra_command_args": {
                "cli_args": ["memory", "-l", "60"],
                "type": "memory",
            },
            "infra_command_type": "memory",
        }
        helper = GremlinAttackCommandHelper()
        helper.shortType = expected_output["infra_command_type"]

        helper_output = helper.impact_definition_graph()
        self.assertEqual(helper_output, expected_output)

    def test__port_maker(self) -> None:
        expected_output = []
        helper = GremlinNetworkAttackHelper()
        helper_output = helper._port_maker()
        self.assertEqual(expected_output, helper_output)

        expected_output = ["80"]
        helper = GremlinNetworkAttackHelper()
        helper_output = helper._port_maker(80)
        self.assertEqual(expected_output, helper_output)

        expected_output = ["8080", "433", "23"]
        helper = GremlinNetworkAttackHelper()
        helper_output = helper._port_maker(expected_output)
        self.assertEqual(expected_output, helper_output)

    # GremlinCPUAttack
    # GremlinMemoryAttack
    # GremlinDiskSpaceAttack
    # GremlinDiskIOAttack
    # GremlinShutdownAttack
    # GremlinProcessKillerAttack
    # GremlinTimeTravelAttack
    # GremlinBlackholeAttack
    # GremlinLatencyAttack
    # GremlinPacketLossAttack
    # def test_list_endpoint(self) -> None:
    #     test_endpoint = "test-endpoint.com"
    #     expected_output = "%s/?source=scenario&pageSize=3&" % test_endpoint
    #     test_kwargs = {"source":"scenario","pageSize":3}
    #     test_output = GremlinAPIAttacks._list_endpoint(test_endpoint,**test_kwargs)
    #     self.assertEqual(test_output, expected_output)
    # @patch('requests.post')
    # def test_create_attack_with_decorator(self, mock_get) -> None:
    #     expected_output_class = GremlinAttackHelper()
    #     test_kwargs = {"body":expected_output_class}
    #     mock_get.return_value = requests.Response()
    #     mock_get.return_value.status_code = 200
    #     mock_get.return_value.json = mock_json
    #     self.assertEqual(GremlinAPIAttacks.create_attack(**test_kwargs), mock_data)
