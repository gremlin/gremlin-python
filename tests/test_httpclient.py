# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>
#
# import json
# import os
# import pickle
# import sys
# import tempfile
# import unittest
#
#
# parentPath = os.path.abspath("..")
# if parentPath not in sys.path:
#     sys.path.insert(0, parentPath)
#
# from gremlinapi.config import GremlinAPIConfig as config
# from gremlinapi.http_clients import get_gremlin_httpclient
#
# api_key = 'api-key-string'
# bearer_token = 'bearer-token-string'
#
# class TestHttpClient(unittest.TestCase):
#
#     def test_api_key(self):
#         config.api_key = api_key
#         https_client = get_gremlin_httpclient()
#         header = https_client.header()
#         self.assertIn(api_key, header['Authorization'])
#
#     def test_bearer_token(self):
#         config.bearer_token = bearer_token
#         https_client = get_gremlin_httpclient()
#         header = https_client.header()
#         self.assertIn(bearer_token, header['Authorization'])
#
#
# if __name__ == '__main__':
#     unittest.main()
