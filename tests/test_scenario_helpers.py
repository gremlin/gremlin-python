import unittest
from unittest.mock import patch
import logging
import requests
import json
import uuid

from gremlinapi.scenario_helpers import GremlinScenarioHelper, GremlinILFIStep

from .util import mock_json, mock_data, mock_scenario, mock_scenario_step


class TestScenarioHelpers(unittest.TestCase):
    def test_gremlin_scenario_helper_add_step(self) -> None:
        helper = GremlinScenarioHelper(**mock_scenario)
        helper_step = GremlinILFIStep(**mock_scenario_step)
        helper_step_2 = GremlinILFIStep(**mock_scenario_step)

        self.assertEqual(len(helper.steps), 0)
        helper.add_step(helper_step)
        self.assertEqual(len(helper.steps), 1)
        helper.add_step(helper_step_2)
        self.assertEqual(len(helper.steps), 2)

        self.assertEqual(helper.steps[0], json.loads(str(helper_step)))
        self.assertEqual(helper.steps[1], json.loads(str(helper_step_2)))

    def test_gremlin_scenario_helper_repr_model(self) -> None:
        helper = GremlinScenarioHelper(**mock_scenario)
        helper_step = GremlinILFIStep(**mock_scenario_step)
        helper_step_2 = GremlinILFIStep(**mock_scenario_step)

        helper.add_step(helper_step)
        helper.add_step(helper_step_2)

        expected_output = {
            "description": mock_scenario["description"],
            "hypothesis": mock_scenario["hypothesis"],
            "name": mock_scenario["name"],
            "steps": [json.loads(str(helper_step)), json.loads(str(helper_step_2))],
        }

        self.assertEqual(repr(helper), json.dumps(expected_output))

    def test_step_and_ilfi_step_repr_model(self) -> None:
        helper = GremlinILFIStep(**mock_scenario_step)

        expected_attacks = [
            {
                "attackType": "ILFI",
                "impactDefinition": mock_scenario_step["command"].impact_definition(),
                "targetDefinition": mock_scenario_step["target"].target_definition(),
            }
        ]
        expected_output = {
            "delay": mock_scenario_step["delay"],
            "attacks": expected_attacks,
            "id": str(uuid.uuid3(uuid.NAMESPACE_X500, str(expected_attacks))),
        }

        self.assertEqual(repr(helper), json.dumps(expected_output))
