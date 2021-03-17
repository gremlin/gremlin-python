import unittest
from unittest.mock import patch
import logging
import requests
import gremlinapi.cli as cli

# from gremlinapi.attacks import GremlinAPIAttacks
# from gremlinapi.attack_helpers import GremlinAttackHelper, GremlinTargetContainers, GremlinLatencyAttack

from .util import mock_json, mock_data


class TestCLI(unittest.TestCase):
    def test_register_cli_action(self) -> None:
        pass

    def test__base_args(self) -> None:
        pass

    def test__get_parser(self) -> None:
        pass

    def test__parse_args(self) -> None:
        pass

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
