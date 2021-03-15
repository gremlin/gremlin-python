# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Kyle Bouchard <kyle.bouchard@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import unittest
import requests
import logging
from unittest.mock import patch
from gremlinapi.attacks import GremlinAPIAttacks
from gremlinapi.attack_helpers import (
    GremlinAttackHelper,
    GremlinTargetContainers,
    GremlinLatencyAttack,
)

from .util import mock_json, mock_data


class TestAttacks(unittest.TestCase):
    def test_list_endpoint(self) -> None:
        test_endpoint = "test-endpoint.com"
        expected_output = "%s/?source=scenario&pageSize=3&" % test_endpoint
        test_kwargs = {"source": "scenario", "pageSize": 3}
        test_output = GremlinAPIAttacks._list_endpoint(test_endpoint, **test_kwargs)
        self.assertEqual(test_output, expected_output)

    def test_error_if_not_attack_body(self) -> None:
        expected_output_class = GremlinAttackHelper()
        test_kwargs = {"body": expected_output_class}
        test_output = GremlinAPIAttacks._error_if_not_attack_body(**test_kwargs)
        self.assertEqual(test_output, str(expected_output_class))

    @patch("requests.post")
    def test_create_attack_with_decorator(self, mock_get) -> None:
        expected_output_class = GremlinAttackHelper()
        test_kwargs = {"body": expected_output_class}
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIAttacks.create_attack(**test_kwargs), mock_data)

    @patch("requests.get")
    def test_list_active_attacks_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIAttacks.list_active_attacks(), mock_data)

    @patch("requests.get")
    def test_list_attacks_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIAttacks.list_attacks(), mock_data)

    @patch("requests.get")
    def test_list_completed_attacks_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIAttacks.list_completed_attacks(), mock_data)

    @patch("requests.get")
    def test_get_attack_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        test_kwargs = {"guid": "1234567890"}
        self.assertEqual(GremlinAPIAttacks.get_attack(**test_kwargs), mock_data)

    @patch("requests.delete")
    def test_halt_all_attacks_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinAPIAttacks.halt_all_attacks(), mock_data)

    @patch("requests.delete")
    def test_halt_attack_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        test_kwargs = {"guid": "1234567890"}
        self.assertEqual(GremlinAPIAttacks.halt_attack(**test_kwargs), mock_data)
