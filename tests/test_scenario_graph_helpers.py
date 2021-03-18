import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.scenario_graph_helpers import (
    GremlinScenarioGraphHelper,
    GremlinScenarioNode,
    # GremlinScenarioAttackNode,
    GremlinScenarioILFINode,
    # GremlinScenarioALFINode,
    GremlinScenarioDelayNode,
    GremlinScenarioStatusCheckNode,
    _GremlinNodeGraph,
)

from .util import mock_json, mock_data, mock_scenario, mock_ilfi_node, mock_delay_node


class TestScenarioGraphHelpers(unittest.TestCase):
    def test_add_node(self) -> None:
        helper = GremlinScenarioGraphHelper(**mock_scenario)
        helper_node = GremlinScenarioNode(**mock_scenario)
        helper_node_2 = GremlinScenarioNode(**mock_scenario)
        helper.add_node(helper_node)
        helper.add_node(helper_node_2)
        self.assertEqual(helper._nodes.get_node(0), helper_node)
        self.assertNotEqual(helper._nodes.get_node(0), helper_node_2)

    def test_gremlin_scenario_graph_helper_repr_model(self) -> None:
        helper = GremlinScenarioGraphHelper(**mock_scenario)
        self.assertEqual(helper.repr_model(), mock_scenario)

    def test_add_edge(self) -> None:
        helper = GremlinScenarioNode(**mock_scenario)
        helper_2 = GremlinScenarioNode(**mock_scenario)

        self.assertEqual(len(helper._edges), 0)

        helper.add_edge(helper_2)

        self.assertEqual(len(helper._edges), 1)
        self.assertEqual(helper._edges[helper_2.id]["node"], helper_2)

    def test_gremlin_scenario_node_repr_model(self) -> None:
        helper = GremlinScenarioNode(**mock_scenario)
        expected_output = {
            "id": "mock_scenario-%s" % helper.id,
            "next": None,
            "type": helper.node_type,
        }

        self.assertEqual(helper.repr_model(), expected_output)

    def test_gremlin_scenario_ilfi_node_repr_node(self) -> None:
        helper = GremlinScenarioILFINode(**mock_ilfi_node)
        expected_output = {
            "id": "mock_scenario-%s" % helper.id,
            "impact_definition": {
                "infra_command_args": {"cli_args": ["", "-l", "60"], "type": ""},
                "infra_command_type": "",
            },
            "next": None,
            "target_definition": {
                "strategy": {"percentage": 10, "type": "RandomPercent"},
                "strategy_type": "Random",
            },
            "type": "InfraAttack",
        }

        self.assertEqual(helper.repr_model(), expected_output)

    def test_gremlin_scenario_delay_node_repr_node(self) -> None:
        helper = GremlinScenarioDelayNode(**mock_delay_node)
        expected_output = {
            "delay": "42",
            "id": "Delay-%s" % helper.id,
            "next": None,
            "type": "Delay",
        }

        self.assertEqual(helper.repr_model(), expected_output)

    # @patch('requests.post')
    # def test_create_attack_with_decorator(self, mock_get) -> None:
    #     expected_output_class = GremlinAttackHelper()
    #     test_kwargs = {"body":expected_output_class}
    #     mock_get.return_value = requests.Response()
    #     mock_get.return_value.status_code = 200
    #     mock_get.return_value.json = mock_json
    #     self.assertEqual(GremlinAPIAttacks.create_attack(**test_kwargs), mock_data)
