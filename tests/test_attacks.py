# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Kyle Bouchard <kyle.bouchard@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import unittest
import json
import requests
import logging
from unittest.mock import patch
from unittest.mock import MagicMock, Mock, PropertyMock
import gremlinapi
from gremlinapi.attacks import GremlinAPIAttacks
from gremlinapi.attack_helpers import GremlinAttackHelper, GremlinTargetContainers, GremlinLatencyAttack
import gremlinapi.http_clients

log = logging.getLogger("GremlinAPI.unit_tests")
log.setLevel(logging.DEBUG)

mock_data = {"testkey":"testval"}
def mock_json():
    return mock_data

class TestAttacks(unittest.TestCase):
    @patch('requests.get')
    def test_list_attacks_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIAttacks.list_attacks(),mock_data)
    
    @patch('requests.get')
    def test_list_active_attacks_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIAttacks.list_active_attacks(),mock_data)

    def test_list_endpoint(self) -> None:
        test_endpoint = "test-endpoint.com"        
        expected_output = "%s/?source=scenario&pageSize=3&" % test_endpoint
        test_kwargs = {"source":"scenario","pageSize":3}
        test_output = GremlinAPIAttacks._list_endpoint(test_endpoint,**test_kwargs)
        self.assertEqual(test_output, expected_output)

    def test_error_if_not_attack_body(self) -> None:
        # expected_output = GremlinAttackHelper(target=GremlinTargetContainers(strategy_type='Random', labels={'owner': 'kyle'}, percent=100),command=GremlinLatencyAttack(delay=1))
        expected_output = "expected string output"
        test_kwargs = {"body":expected_output}      
        test_output = GremlinAPIAttacks._error_if_not_attack_body(**test_kwargs)
        self.assertEqual(test_output, expected_output)