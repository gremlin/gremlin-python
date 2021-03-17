# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import unittest
from unittest.mock import patch
import logging
import requests
from gremlinapi.gremlinapi import GremlinAPI
import gremlinapi.exceptions as g_exceptions
from gremlinapi.config import GremlinAPIConfig

from .util import mock_json, mock_data, mock_team_id

test_param = 'myparam'
test_value = 'paramval'
test_params = ['myparam', 'anotherparam','team_id']
test_kwargs = {'myparam':'param1val','anotherparam':'param2val','team_id':mock_team_id}

test_base_endpoint = "test-endpoint.com"

class TestAPI(unittest.TestCase):
    def test__add_query_param(self) -> None:
        test_endpoint = "%s/?&dummy=yes" % test_base_endpoint
        expected_output = '%s&%s=%s' % (test_endpoint,test_param,test_value)
        self.assertEqual(GremlinAPI._add_query_param(test_endpoint, test_param, test_value), expected_output)

        test_endpoint = "%s/?&dummy=yes&" % test_base_endpoint
        expected_output = '%s%s=%s' % (test_endpoint,test_param,test_value)
        self.assertEqual(GremlinAPI._add_query_param(test_endpoint, test_param, test_value), expected_output)

        test_endpoint = "%s" % test_base_endpoint
        expected_output = '%s/?%s=%s' % (test_endpoint,test_param,test_value)
        self.assertEqual(GremlinAPI._add_query_param(test_endpoint, test_param, test_value), expected_output)

    def test__build_query_string_endpoint(self) -> None:
        test_endpoint = "%s" % test_base_endpoint
        expected_output = '%s/?%s=%s&%s=%s&%s=%s' % (test_endpoint,test_params[0],test_kwargs[test_params[0]],test_params[1], test_kwargs[test_params[1]],test_params[2],test_kwargs[test_params[2]])
        self.assertEqual(GremlinAPI._build_query_string_endpoint(test_endpoint,test_params,**test_kwargs), expected_output)
        
    def test__build_query_string_option_team_endpoint(self) -> None:
        test_endpoint = "%s" % test_base_endpoint
        expected_output = '%s/?%s=%s&%s=%s&%s=%s' % (test_endpoint,test_params[0],test_kwargs[test_params[0]],test_params[1], test_kwargs[test_params[1]],test_params[2],test_kwargs[test_params[2]])
        self.assertEqual(GremlinAPI._build_query_string_option_team_endpoint(test_endpoint,test_params,**test_kwargs), expected_output)
        
    def test__build_query_string_required_team_endpoint(self) -> None:
        test_endpoint = "%s" % test_base_endpoint
        expected_output = '%s/?%s=%s&%s=%s&%s=%s' % (test_endpoint,test_params[0],test_kwargs[test_params[0]],test_params[1], test_kwargs[test_params[1]],test_params[2],test_kwargs[test_params[2]])
        self.assertEqual(GremlinAPI._build_query_string_required_team_endpoint(test_endpoint,test_params,**test_kwargs), expected_output)
        
    def test__optional_team_endpoint(self) -> None:
        test_endpoint = "%s" % test_base_endpoint
        
        expected_output = '%s/?%s=%s' % (test_endpoint,test_params[2],test_kwargs[test_params[2]])
        self.assertEqual(GremlinAPI._optional_team_endpoint(test_endpoint,**test_kwargs), expected_output)

        expected_output = '%s' % (test_endpoint)
        self.assertEqual(GremlinAPI._optional_team_endpoint(test_endpoint), expected_output)

    def test__required_team_endpoint(self) -> None:
        test_endpoint = "%s" % test_base_endpoint
       
        try:
            GremlinAPI._required_team_endpoint(test_endpoint)
        except g_exceptions.GremlinParameterError as gpe:
            self.assertEqual("Endpoint requires a team_id, none supplied", str(gpe))
            
        
        
  


    # def test_list_endpoint(self) -> None:
    #     test_endpoint = "test-endpoint.com"        
    #     expected_output = "%s/?source=scenario&pageSize=3&" % test_endpoint
    #     test_kwargs = {"source":"scenario","pageSize":3}
    #     self.assertEqual(GremlinAPI._build_query_string_endpoint(test_endpoint,**test_kwargs), expected_output)
    # @patch('requests.post')
    # def test_create_attack_with_decorator(self, mock_get) -> None:
    #     expected_output_class = GremlinAPI()
    #     test_kwargs = {"body":expected_output_class}
    #     mock_get.return_value = requests.Response()
    #     mock_get.return_value.status_code = 200
    #     mock_get.return_value.json = mock_json
    #     self.assertEqual(GremlinAPI.create_attack(**test_kwargs), mock_data)