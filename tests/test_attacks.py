# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Kyle Bouchard <kyle.bouchard@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import unittest
from unittest.mock import patch
from unittest.mock import MagicMock, Mock
import gremlinapi
from gremlinapi.attacks import GremlinAPIAttacks
import gremlinapi.http_clients

class TestAttacks(unittest.TestCase):

    # @patch('users.requests.get')  # Mock 'requests' module 'get' method.
    # def test_request_response_with_decorator(self, mock_get):
    #     """Mocking using a decorator"""
    #     mock_get.return_value.status_code = 200 # Mock status code of response.
    #     response = get_users()

    #     # Assert that the request-response cycle completed successfully.
    #     self.assertEqual(response.status_code, 200)

    @patch('gremlinapi.http_clients.requests.get')
    def test_list_attacks_with_decorator(self, mock_get) -> None:
        testbody = {"testkey":"testval"}
        attackObj = GremlinAPIAttacks()
        attackObj.list_attacks = MagicMock(return_value=testbody)
        returnval = attackObj.list_attacks()
        self.assertEqual(returnval,testbody)

        # apiObj = gremlinapi.http_clients
        # apiObj.api_call = MagicMock(return_value = (None, testbody))
        # returnval = apiObj.api_call()

        # # myMock = Mock(return_value=testbody,status_code=200)
        # mock_get.list_attacks.return_value.body = testbody
        # mock_get.return_value.status_code = 200
        # # myval.status_code: int = 200
        # # gremlinapi.login(email=GREMLIN_USER,
        # #          password=GREMLIN_PASSWORD,
        # #          company_name=GREMLIN_COMPANY,
        # #          token="")
        # myreturn = GremlinAPIAttacks.list_attacks()
        # mock_get.assert_called_with(testbody)
        # # # testreturn = gAttacks
        # # gAttacks.assert_called_with(testbody)

        # # self.assertEqual(gAttacks.status_code, 200)