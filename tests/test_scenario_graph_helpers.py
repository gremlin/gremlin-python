import unittest
from unittest.mock import patch
import logging
from gremlinapi.scenario_graph_helpers import (
    GremlinScenarioGraphHelper,
    GremlinScenarioNode,
    GremlinScenarioSerialNode,
    GremlinScenarioParallelNode,
    GremlinScenarioAttackNode,
    GremlinScenarioILFINode,
    GremlinScenarioALFINode,
    GremlinScenarioDelayNode,
    GremlinScenarioStatusCheckNode,
    _GremlinNodeGraph,
)

from gremlinapi.attack_helpers import (
    GremlinAttackTargetHelper,
    GremlinAttackCommandHelper,
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

    def test_gremlin_scenario_graph_helper_api_model(self) -> None:
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
        new_node = GremlinScenarioStatusCheckNode(
            description=status_check_description,
            endpoint_url=endpoint_url,
            endpoint_headers=endpoint_headers,
            evaluation_ok_status_codes=evaluation_ok_status_codes,
            evaluation_ok_latency_max=evaluation_ok_latency_max,
            evaluation_response_body_evaluation=evaluation_response_body_evaluation,
        )
        my_scenario.add_node(new_node)
        new_node_2 = GremlinScenarioStatusCheckNode(
            description=status_check_description,
            endpoint_url=endpoint_url,
            endpoint_headers=endpoint_headers,
            evaluation_ok_status_codes=evaluation_ok_status_codes,
            evaluation_ok_latency_max=evaluation_ok_latency_max,
            evaluation_response_body_evaluation=evaluation_response_body_evaluation,
        )
        my_scenario.add_node(new_node_2)
        new_node_3 = GremlinScenarioDelayNode(
            description="Add some delay", delay=delay_time
        )
        my_scenario.add_node(new_node_3)
        new_node_4 = GremlinScenarioStatusCheckNode(
            description=status_check_description,
            endpoint_url=endpoint_url,
            endpoint_headers=endpoint_headers,
            evaluation_ok_status_codes=evaluation_ok_status_codes,
            evaluation_ok_latency_max=evaluation_ok_latency_max,
            evaluation_response_body_evaluation=evaluation_response_body_evaluation,
        )
        my_scenario.add_node(new_node_4)
        my_scenario.add_edge(new_node, new_node_3)
        my_scenario.add_edge(new_node_2, new_node_4)
        my_scenario.add_edge(new_node_3, new_node_2)
        t_diff = self.maxDiff
        self.maxDiff = None
        expected_output = {
            "description": "Three nodes now",
            "graph": {
                "nodes": {
                    "0": {
                        "endpointConfiguration": {
                            "headers": {"Authorization": "mock-auth"},
                            "url": "https://www.google.com",
                        },
                        "evaluationConfiguration": {
                            "okLatencyMaxMs": 1000,
                            "okStatusCodes": ["404", "300"],
                            "responseBodyEvaluation": {"op": "AND", "predicates": []},
                        },
                        "guid": "status-check-%s" % new_node.id,
                        "id": "0",
                        "next": "1",
                        "thirdPartyPresets": "PythonSDK",
                        "type": "SynchronousStatusCheck",
                    },
                    "1": {
                        "delay": 5,
                        "guid": "Delay-%s" % new_node_3.id,
                        "type": "Delay",
                        "id": "1",
                        "next": "2",
                    },
                    "2": {
                        "endpointConfiguration": {
                            "headers": {"Authorization": "mock-auth"},
                            "url": "https://www.google.com",
                        },
                        "evaluationConfiguration": {
                            "okLatencyMaxMs": 1000,
                            "okStatusCodes": ["404", "300"],
                            "responseBodyEvaluation": {"op": "AND", "predicates": []},
                        },
                        "guid": "status-check-%s" % new_node_2.id,
                        "id": "2",
                        "next": "3",
                        "thirdPartyPresets": "PythonSDK",
                        "type": "SynchronousStatusCheck",
                    },
                    "3": {
                        "endpointConfiguration": {
                            "headers": {"Authorization": "mock-auth"},
                            "url": "https://www.google.com",
                        },
                        "evaluationConfiguration": {
                            "okLatencyMaxMs": 1000,
                            "okStatusCodes": ["404", "300"],
                            "responseBodyEvaluation": {"op": "AND", "predicates": []},
                        },
                        "guid": "status-check-%s" % new_node_4.id,
                        "id": "3",
                        "next": "4",
                        "thirdPartyPresets": "PythonSDK",
                        "type": "SynchronousStatusCheck",
                    },
                },
                "start_id": "0",
            },
            "hypothesis": "No Hypothesis",
            "name": "code_created_scenario_6",
        }
        self.assertEqual(my_scenario.api_model(), expected_output)
        self.maxDiff = t_diff

    def test_gremlin_scenario_graph_helper_repr_str(self) -> None:
        expected_output = 'GremlinScenarioGraphHelper({"name": "code_created_scenario_6", "description": "Three nodes now", "hypothesis": "No Hypothesis"})'
        kwargs = {
            "name": "code_created_scenario_6",
            "description": "Three nodes now",
            "hypothesis": "No Hypothesis",
        }
        helper = GremlinScenarioGraphHelper(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    def test_gremlin_scenario_graph_helper_api_model_default_add_node(self) -> None:
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
        new_node = GremlinScenarioStatusCheckNode(
            description=status_check_description,
            endpoint_url=endpoint_url,
            endpoint_headers=endpoint_headers,
            evaluation_ok_status_codes=evaluation_ok_status_codes,
            evaluation_ok_latency_max=evaluation_ok_latency_max,
            evaluation_response_body_evaluation=evaluation_response_body_evaluation,
        )
        my_scenario.add_node(new_node, True)
        new_node_2 = GremlinScenarioStatusCheckNode(
            description=status_check_description,
            endpoint_url=endpoint_url,
            endpoint_headers=endpoint_headers,
            evaluation_ok_status_codes=evaluation_ok_status_codes,
            evaluation_ok_latency_max=evaluation_ok_latency_max,
            evaluation_response_body_evaluation=evaluation_response_body_evaluation,
        )
        my_scenario.add_node(new_node_2, True)
        new_node_3 = GremlinScenarioDelayNode(
            description="Add some delay", delay=delay_time
        )
        my_scenario.add_node(new_node_3, True)
        new_node_4 = GremlinScenarioStatusCheckNode(
            description=status_check_description,
            endpoint_url=endpoint_url,
            endpoint_headers=endpoint_headers,
            evaluation_ok_status_codes=evaluation_ok_status_codes,
            evaluation_ok_latency_max=evaluation_ok_latency_max,
            evaluation_response_body_evaluation=evaluation_response_body_evaluation,
        )
        my_scenario.add_node(new_node_4, True)
        t_diff = self.maxDiff
        self.maxDiff = None
        expected_output = {
            "description": "Three nodes now",
            "graph": {
                "nodes": {
                    "0": {
                        "endpointConfiguration": {
                            "headers": {"Authorization": "mock-auth"},
                            "url": "https://www.google.com",
                        },
                        "evaluationConfiguration": {
                            "okLatencyMaxMs": 1000,
                            "okStatusCodes": ["404", "300"],
                            "responseBodyEvaluation": {"op": "AND", "predicates": []},
                        },
                        "guid": "status-check-%s" % new_node.id,
                        "id": "0",
                        "next": "1",
                        "thirdPartyPresets": "PythonSDK",
                        "type": "SynchronousStatusCheck",
                    },
                    "1": {
                        "endpointConfiguration": {
                            "headers": {"Authorization": "mock-auth"},
                            "url": "https://www.google.com",
                        },
                        "evaluationConfiguration": {
                            "okLatencyMaxMs": 1000,
                            "okStatusCodes": ["404", "300"],
                            "responseBodyEvaluation": {"op": "AND", "predicates": []},
                        },
                        "guid": "status-check-%s" % new_node_2.id,
                        "id": "1",
                        "next": "2",
                        "thirdPartyPresets": "PythonSDK",
                        "type": "SynchronousStatusCheck",
                    },
                    "2": {
                        "delay": 5,
                        "guid": "Delay-%s" % new_node_3.id,
                        "id": "2",
                        "next": "3",
                        "type": "Delay",
                    },
                    "3": {
                        "endpointConfiguration": {
                            "headers": {"Authorization": "mock-auth"},
                            "url": "https://www.google.com",
                        },
                        "evaluationConfiguration": {
                            "okLatencyMaxMs": 1000,
                            "okStatusCodes": ["404", "300"],
                            "responseBodyEvaluation": {"op": "AND", "predicates": []},
                        },
                        "guid": "status-check-%s" % new_node_4.id,
                        "id": "3",
                        "next": "4",
                        "thirdPartyPresets": "PythonSDK",
                        "type": "SynchronousStatusCheck",
                    },
                },
                "start_id": "0",
            },
            "hypothesis": "No Hypothesis",
            "name": "code_created_scenario_6",
        }
        self.assertEqual(my_scenario.api_model(), expected_output)
        self.maxDiff = t_diff

    def test_add_edge(self) -> None:
        helper = GremlinScenarioNode(**mock_scenario)
        helper_2 = GremlinScenarioNode(**mock_scenario)

        self.assertEqual(len(helper._edges), 0)

        helper.add_edge(helper_2)

        self.assertEqual(len(helper._edges), 1)
        self.assertEqual(helper._edges[helper_2.id]["node"], helper_2)

    def test_gremlin_scenario_node_api_model(self) -> None:
        helper = GremlinScenarioNode(**mock_scenario)
        expected_output = {
            "guid": "mock_scenario-%s" % helper.id,
            "id": "0",
            "next": "0",
            "type": helper.node_type,
        }

        self.assertEqual(helper.api_model(), expected_output)

    def test_gremlin_scenario_node_repr_str(self) -> None:
        expected_output = 'GremlinScenarioNode({"name": "a mock node"})'
        kwargs = {
            "name": "a mock node",
        }
        helper = GremlinScenarioNode(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    def test_gremlin_scenario_serial_node_repr_str(self) -> None:
        expected_output = 'GremlinScenarioSerialNode({"name": "a mock serial node"})'
        kwargs = {
            "name": "a mock serial node",
        }
        helper = GremlinScenarioSerialNode(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    def test_gremlin_scenario_parallel_node_repr_str(self) -> None:
        expected_output = (
            'GremlinScenarioParallelNode({"name": "a mock parallel node"})'
        )
        kwargs = {
            "name": "a mock parallel node",
        }
        helper = GremlinScenarioParallelNode(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    def test_gremlin_scenario_attack_node_repr_str(self) -> None:
        expected_output = 'GremlinScenarioAttackNode({"name": "a mock attack node"})'
        kwargs = {
            "name": "a mock attack node",
        }
        helper = GremlinScenarioAttackNode(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    def test_gremlin_scenario_ilfi_node_repr_node(self) -> None:
        helper = GremlinScenarioILFINode(**mock_ilfi_node)
        expected_output = {
            "guid": "mock_scenario-%s" % helper.id,
            "id": "0",
            "next": "0",
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

        self.assertEqual(helper.api_model(), expected_output)

    def test_gremlin_scenario_ilfi_node_repr_str(self) -> None:
        expected_output = "GremlinScenarioILFINode({'name': 'mock_scenario', 'command': 'GremlinAttackCommandHelper({\"length\": 70})', 'target': 'GremlinAttackTargetHelper({\"exact\": 0, \"percent\": 15, \"strategy_type\": \"Random\"})'})"
        kwargs_ch = {"length": 70}
        kwargs_th = {"exact": 0, "percent": 15, "strategy_type": "Random"}
        kwargs = {
            "name": "mock_scenario",
            "command": GremlinAttackCommandHelper(**kwargs_ch),
            "target": GremlinAttackTargetHelper(**kwargs_th),
        }
        helper = GremlinScenarioILFINode(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    # def test_gremlin_scenario_alfi_node_repr_str(self) -> None:
    #     expected_output = 'GremlinScenarioALFINode({"name": "a mock alfi node"})'
    #     kwargs = {
    #         "name": "a mock alfi node",
    #     }
    #     helper = GremlinScenarioALFINode(**kwargs)
    #     helper_output = repr(helper)
    #     self.assertEqual(expected_output, helper_output)
    #     helper_output = str(helper)
    #     self.assertEqual(expected_output, helper_output)

    def test_gremlin_scenario_delay_node_repr_str(self) -> None:
        expected_output = (
            'GremlinScenarioDelayNode({"name": "a mock delay node", "delay": 100})'
        )
        kwargs = {
            "name": "a mock delay node",
            "delay": 100,
        }
        helper = GremlinScenarioDelayNode(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    def test_gremlin_scenario_status_check_node_repr_str(self) -> None:
        expected_output = 'GremlinScenarioStatusCheckNode({"name": "a mock status check node", "description": "A mock description", "endpoint_url": "www.example.com", "endpoint_headers": {}, "evaluation_ok_status_codes": ["300-400"], "evaluation_ok_latency_max": 1000, "evaluation_response_body_evaluation": "a mock resposne body"})'
        kwargs = {
            "name": "a mock status check node",
            "description": "A mock description",
            "endpoint_url": "www.example.com",
            "endpoint_headers": {},
            "evaluation_ok_status_codes": ["300-400"],
            "evaluation_ok_latency_max": 1000,
            "evaluation_response_body_evaluation": "a mock resposne body",
        }
        helper = GremlinScenarioStatusCheckNode(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    def test_gremlin_scenario_delay_node_repr_node(self) -> None:
        helper = GremlinScenarioDelayNode(**mock_delay_node)
        expected_output = {
            "delay": "42",
            "guid": "Delay-%s" % helper.id,
            "id": "0",
            "next": "0",
            "type": "Delay",
        }

        self.assertEqual(helper.api_model(), expected_output)

    def test_gremlin_scenario_status_check_node_api_model(self) -> None:
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
            "guid": "status-check-%s" % helper.id,
            "id": "0",
            "next": "0",
            "thirdPartyPresets": "PythonSDK",
            "type": "SynchronousStatusCheck",
        }
        self.assertEqual(helper.api_model(), expected_output)

    def test_node_graph_repr_str(self) -> None:
        expected_output = "_GremlinNodeGraph()"
        kwargs = {}
        helper = _GremlinNodeGraph(**kwargs)
        helper_output = repr(helper)
        self.assertEqual(expected_output, helper_output)
        helper_output = str(helper)
        self.assertEqual(expected_output, helper_output)

    def test_node_graph_add_edge(self) -> None:
        helper = _GremlinNodeGraph()
        helper_node = GremlinScenarioNode(**mock_scenario)
        helper_node_2 = GremlinScenarioNode(**mock_scenario)

        self.assertEqual(len(helper_node_2._edges), 0)
        self.assertEqual(len(helper_node._edges), 0)
        helper.add_edge(helper_node, helper_node_2)
        self.assertEqual(helper_node_2._edges[helper_node.id]["node"], helper_node)
        self.assertEqual(helper_node._edges[helper_node_2.id]["node"], helper_node_2)

    def test_gremlin_scenario_helper_remove_edge(self) -> None:
        helper = GremlinScenarioGraphHelper(
            name="code_created_scenario_6",
            description="Three nodes now",
            hypothesis="No Hypothesis",
        )
        helper_node = GremlinScenarioNode(**mock_scenario)
        helper_node_2 = GremlinScenarioNode(**mock_scenario)
        helper_node_3 = GremlinScenarioNode(**mock_scenario)

        helper.add_node(helper_node)
        helper.add_node(helper_node_2)
        helper.add_node(helper_node_3)

        # insert between
        # remove_edge
        # {helper_node} <-> {helper_node_2} <-> {helper_node_3}
        helper.add_edge(helper_node, helper_node_2)
        helper.add_edge(helper_node_2, helper_node_3)
        self.assertFalse(helper_node.id in helper_node_3._edges)
        self.assertFalse(helper_node_3.id in helper_node._edges)
        self.assertTrue(helper_node.id in helper_node_2._edges)
        self.assertTrue(helper_node_2.id in helper_node._edges)
        self.assertTrue(helper_node_2.id in helper_node_3._edges)
        self.assertTrue(helper_node_3.id in helper_node_2._edges)

        helper.remove_edge(helper_node_2)
        self.assertFalse(helper_node.id in helper_node_2._edges)
        self.assertFalse(helper_node_2.id in helper_node._edges)
        self.assertFalse(helper_node_2.id in helper_node_3._edges)
        self.assertFalse(helper_node_3.id in helper_node_2._edges)

        helper.add_edge(helper_node, helper_node_2)
        self.assertTrue(helper_node.id in helper_node_2._edges)
        self.assertTrue(helper_node_2.id in helper_node._edges)

        helper.remove_edge(helper_node, helper_node_2)
        self.assertFalse(helper_node.id in helper_node_2._edges)
        self.assertFalse(helper_node_2.id in helper_node._edges)

    def test__gremlin_node_graph_functions(self) -> None:
        helper = _GremlinNodeGraph()
        helper_node = GremlinScenarioNode(**mock_scenario)
        helper_node_2 = GremlinScenarioNode(**mock_scenario)
        helper_node_3 = GremlinScenarioNode(**mock_scenario)
        helper_node_4 = GremlinScenarioNode(**mock_scenario)

        # append first node
        # {helper_node}
        self.assertEqual(helper.head, None)
        helper.append(helper_node)
        self.assertEqual(helper.head, helper_node)

        # append second node
        # add_edge
        # {helper_node} <-> {helper_node_2}
        helper.append(helper_node_2)
        helper.add_edge(helper_node, helper_node_2)
        self.assertEqual(helper.head._edges[helper_node_2.id]["node"], helper_node_2)
        self.assertEqual(helper_node_2._edges[helper.head.id]["node"], helper.head)
        self.assertEqual(helper_node._edges[helper_node_2.id]["node"], helper_node_2)
        self.assertEqual(helper_node_2._edges[helper_node.id]["node"], helper_node)

        # insert between
        # remove_edge
        # {helper_node} <-> {helper_node_3} <-> {helper_node_2}
        helper.append(helper_node_3)
        helper.remove_edge(helper_node, helper_node_2)
        helper.add_edge(helper_node, helper_node_3)
        helper.add_edge(helper_node_3, helper_node_2)
        self.assertFalse(helper_node_2.id in helper_node._edges)
        self.assertFalse(helper_node.id in helper_node_2._edges)
        self.assertTrue(helper_node.id in helper_node_3._edges)
        self.assertTrue(helper_node_3.id in helper_node._edges)
        self.assertTrue(helper_node_2.id in helper_node_3._edges)
        self.assertTrue(helper_node_3.id in helper_node_2._edges)

        # get_node
        self.assertEqual(helper_node, helper.get_node(helper_node.id))
        self.assertEqual(helper_node_2, helper.get_node(helper_node_2.id))

        # push
        # {helper_node_4} <-> {helper_node} <-> {helper_node_3} <-> {helper_node_2}
        helper.push(helper_node_4)
        self.assertEqual(helper.head, helper_node_4)
        self.assertTrue(helper_node.id in helper_node_4._edges)
        self.assertTrue(helper_node_4.id in helper_node._edges)

        # remove
        # {helper_node_4} <-> {helper_node} <-> {helper_node_2}
        self.assertEqual(helper.get_node(helper_node_3.id), helper_node_3)
        helper.remove(helper_node_3)
        self.assertEqual(helper.get_node(helper_node_3.id), None)
        self.assertFalse(helper_node.id in helper_node_3._edges)
        self.assertFalse(helper_node_3.id in helper_node._edges)
        self.assertFalse(helper_node_2.id in helper_node_3._edges)
        self.assertFalse(helper_node_3.id in helper_node_2._edges)
