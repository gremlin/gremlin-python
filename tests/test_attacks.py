# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Kyle Bouchard <kyle.bouchard@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import unittest
import json
import requests
from unittest.mock import patch
from unittest.mock import MagicMock, Mock, PropertyMock
import gremlinapi
from gremlinapi.attacks import GremlinAPIAttacks
import gremlinapi.http_clients

class TestAttacks(unittest.TestCase):
    @patch('requests.get')
    def test_list_attacks_with_decorator(self, mock_get) -> None:
        mock_data = {"testkey":"testval"}
        def mock_json():
            return mock_data

        mock_get.return_value = requests.Response()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json = mock_json

        self.assertEqual(GremlinAPIAttacks.list_attacks(),mock_data)