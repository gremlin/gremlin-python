import unittest
from unittest.mock import patch
import logging
from gremlinapi.scenario_graph_helpers import (
    GremlinScenarioGraphHelper,
    GremlinScenarioNode,
    GremlinScenarioILFINode,
    GremlinScenarioDelayNode,
    GremlinScenarioStatusCheckNode,
    _GremlinNodeGraph,
)

from .util import (
    mock_scenario,
    mock_ilfi_node,
    mock_delay_node,
    mock_status_check_node,
)


class TestScenarioGraphHelpers(unittest.TestCase):
    def test_add_node(self) -> None:
        helper = GremlinScenarioGraphHelper(**mock_scenario)
        helper_node = GremlinScenarioNode(**mock_scenario)
        helper_node_2 = GremlinScenarioNode(**mock_scenario)
        helper.add_node(helper_node)
        helper.add_node(helper_node_2)
        self.assertEqual(helper._nodes.get_node(helper_node.id), helper_node)
        self.assertNotEqual(helper._nodes.get_node(helper_node.id), helper_node_2)

    def test_gremlin_scenario_graph_helper_repr_model(self) -> None:
        status_check_description = "Check if Gremlin.com is Still Up"
        endpoint_url = "https://www.google.com"
        endpoint_headers = dict()
        endpoint_headers = {"Authorization": "mock-auth"}
        evaluation_ok_status_codes = ["404", "300"]
        evaluation_ok_latency_max = 1000
        evaluation_response_body_evaluation = {"op": "AND", "predicates": []}
        delay_time = 5  # Time to delay between steps in seconds
        my_scenario = GremlinScenarioGraphHelper(
            name="code_created_scenario_6",
            description="Three nodes now",
            hypothesis="No Hypothesis",
        )
        my_scenario.add_node(
            GremlinScenarioStatusCheckNode(
                description=status_check_description,
                endpoint_url=endpoint_url,
                endpoint_headers=endpoint_headers,
                evaluation_ok_status_codes=evaluation_ok_status_codes,
                evaluation_ok_latency_max=evaluation_ok_latency_max,
                evaluation_response_body_evaluation=evaluation_response_body_evaluation,
            )
        )
        my_scenario.add_node(
            GremlinScenarioStatusCheckNode(
                description=status_check_description,
                endpoint_url=endpoint_url,
                endpoint_headers=endpoint_headers,
                evaluation_ok_status_codes=evaluation_ok_status_codes,
                evaluation_ok_latency_max=evaluation_ok_latency_max,
                evaluation_response_body_evaluation=evaluation_response_body_evaluation,
            )
        )
        my_scenario.add_node(
            GremlinScenarioDelayNode(description="Add some delay", delay=delay_time)
        )
        my_scenario.add_node(
            GremlinScenarioStatusCheckNode(
                description=status_check_description,
                endpoint_url=endpoint_url,
                endpoint_headers=endpoint_headers,
                evaluation_ok_status_codes=evaluation_ok_status_codes,
                evaluation_ok_latency_max=evaluation_ok_latency_max,
                evaluation_response_body_evaluation=evaluation_response_body_evaluation,
            )
        )
        t_diff = self.maxDiff
        self.maxDiff = None
        expected_output = {
            "description": "Three nodes now",
            "graph": {
                "nodes": {
                    node.uuid: data
                    for node, data in my_scenario._nodes.nodes_data_linear()
                },
                "start_id": my_scenario._nodes.head.uuid,
            },
            "hypothesis": "No Hypothesis",
            "name": "code_created_scenario_6",
        }
        self.assertEqual(my_scenario.repr_model(), expected_output)
        self.maxDiff = t_diff

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
            # "next": None,
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
            # "next": None,
            "type": "Delay",
        }

        self.assertEqual(helper.repr_model(), expected_output)

    def test_gremlin_scenario_status_check_node_repr_model(self) -> None:
        helper = GremlinScenarioStatusCheckNode(**mock_status_check_node)
        expected_output = {
            "endpointConfiguration": {
                "headers": mock_status_check_node["endpoint_headers"],
                "url": mock_status_check_node["endpoint_url"],
            },
            "evaluationConfiguration": {
                "okLatencyMaxMs": mock_status_check_node["evaluation_ok_latency_max"],
                "okStatusCodes": mock_status_check_node["evaluation_ok_status_codes"],
                "responseBodyEvaluation": mock_status_check_node[
                    "evaluation_response_body_evaluation"
                ],
            },
            "id": "status-check-%s" % helper.id,
            # "next": None,
            "thirdPartyPresets": "PythonSDK",
            "type": "SynchronousStatusCheck",
        }
        self.assertEqual(helper.repr_model(), expected_output)

    def test_node_graph_add_edge(self) -> None:
        helper = _GremlinNodeGraph()
        helper_node = GremlinScenarioNode(**mock_scenario)
        helper_node_2 = GremlinScenarioNode(**mock_scenario)

        self.assertEqual(len(helper_node_2._edges), 0)
        self.assertEqual(len(helper_node._edges), 0)
        helper.add_edge(helper_node, helper_node_2)
        self.assertEqual(helper_node_2._edges[helper_node.id]["node"], helper_node)
        self.assertEqual(helper_node._edges[helper_node_2.id]["node"], helper_node_2)

    def test__gremlin_node_graph_functions(self) -> None:
        helper = _GremlinNodeGraph()
        helper_node = GremlinScenarioNode(**mock_scenario)
        helper_node_2 = GremlinScenarioNode(**mock_scenario)
        helper_node_3 = GremlinScenarioNode(**mock_scenario)
        helper_node_4 = GremlinScenarioNode(**mock_scenario)

        # TODO: validate proper functionality of get_last_node asserted as equal to manual edge adding

        # append
        self.assertEqual(helper.head, None)
        helper.append(helper_node)
        self.assertEqual(helper.head, helper_node)
        # self.assertEqual(helper_node.next, helper_node)
        # self.assertEqual(helper_node.previous, helper_node)

        # insert_after
        # helper.append(helper_node_2)
        # self.assertEqual(helper.head, helper_node)
        # self.assertEqual(helper_node.next, helper_node_2)
        # self.assertEqual(helper_node_2.previous, helper_node)
        # self.assertEqual(helper_node_2.next, helper_node)

        # insert before
        # helper.insert_before(helper_node.next, helper_node_3)
        # self.assertEqual(helper.head, helper_node)
        # self.assertEqual(helper_node.next, helper_node_3)
        # self.assertEqual(helper_node_3.previous, helper_node)
        # self.assertEqual(helper_node_3.next, helper_node_2)
        # self.assertEqual(helper_node_2.previous, helper_node_3)
        # self.assertEqual(helper_node_2.next, helper_node)

        # get_node
        # self.assertEqual(helper_node, helper.get_node(0))
        # self.assertEqual(helper_node_3, helper.get_node(1))
        # self.assertEqual(helper_node_2, helper.get_node(2))

        # push
        # helper.push(helper_node_4)
        # self.assertEqual(helper.head, helper_node_4)
        # self.assertEqual(helper.head.next, helper_node)
        # self.assertEqual(helper_node.previous, helper_node_4)

        # remove
        # self.assertEqual(helper.get_node(2), helper_node_3)
        # helper.remove(helper_node_3)
        # self.assertEqual(helper.get_node(2), helper_node_2)
