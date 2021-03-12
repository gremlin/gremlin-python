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
from gremlinapi.alfi import GremlinALFI
from gremlinapi.attacks import GremlinAPIAttacks
from gremlinapi.attack_helpers import GremlinAttackHelper, GremlinTargetContainers, GremlinLatencyAttack
import gremlinapi.http_clients

log = logging.getLogger("GremlinAPI.unit_tests")
log.setLevel(logging.DEBUG)

mock_data = {"testkey":"testval"}
def mock_json():
    return mock_data
mock_body = {"body":mock_data}
mock_guid = {"guid":mock_data}

class TestAlfi(unittest.TestCase):
    @patch('requests.post')
    def test_create_alfi_experiment_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinALFI.create_alfi_experiment(**mock_body), mock_data)

    @patch('requests.delete')
    def test_halt_all_alfi_experiments_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinALFI.halt_all_alfi_experiments(), mock_data)
    
    @patch('requests.get')
    def test_get_alfi_experiment_details_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinALFI.get_alfi_experiment_details(**mock_guid), mock_data)

    @patch('requests.delete')
    def test_halt_alfi_experiment_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinALFI.halt_alfi_experiment(**mock_guid), mock_data)

    @patch('requests.get')
    def test_list_active_alfi_experiments_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinALFI.list_active_alfi_experiments(), mock_data)

    @patch('requests.get')
    def test_list_completed_alfi_experiments_with_decorator(self, mock_get) -> None:
        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json
        self.assertEqual(GremlinALFI.list_completed_alfi_experiments(), mock_data)
