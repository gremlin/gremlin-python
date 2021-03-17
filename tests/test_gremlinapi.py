# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.gremlinapi import GremlinAPI

from .util import mock_json, mock_data

class TestAPI(unittest.TestCase):
    def test__add_query_param(self) -> None:
        test_endpoint = "test-endpoint.com/?&dummy=yes"
        test_param = 'myparam'
        test_value = 'paramval'
        expected_output = '%s&%s=%s' % (test_endpoint,test_param,test_value)
        self.assertEqual(GremlinAPI._add_query_param(test_endpoint, test_param, test_value), expected_output)

        test_endpoint = "test-endpoint.com/?&dummy=yes&"
        test_param = 'myparam'
        test_value = 'paramval'
        expected_output = '%s%s=%s' % (test_endpoint,test_param,test_value)
        self.assertEqual(GremlinAPI._add_query_param(test_endpoint, test_param, test_value), expected_output)

        test_endpoint = "test-endpoint.com"
        test_param = 'myparam'
        test_value = 'paramval'
        expected_output = '%s/?%s=%s' % (test_endpoint,test_param,test_value)
        self.assertEqual(GremlinAPI._add_query_param(test_endpoint, test_param, test_value), expected_output)

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