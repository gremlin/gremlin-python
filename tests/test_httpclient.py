# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import os
import sys
import unittest

from gremlinapi.config import GremlinAPIConfig as config
from gremlinapi.http_clients import get_gremlin_httpclient, GremlinAPIHttpClient

from .util import api_key, bearer_token

parentPath: str = os.path.abspath("..")
if parentPath not in sys.path:
    sys.path.insert(0, parentPath)


class TestHttpClient(unittest.TestCase):
    def test_api_key(self) -> None:
        config.api_key = api_key
        https_client: GremlinAPIHttpClient = get_gremlin_httpclient()
        header: dict = https_client.header()
        self.assertIn(api_key, header["Authorization"])

    def test_bearer_token(self) -> None:
        config.bearer_token = bearer_token
        https_client: GremlinAPIHttpClient = get_gremlin_httpclient()
        header: dict = https_client.header()
        self.assertIn(bearer_token, header["Authorization"])

    def test_base_uri(self) -> None:
        https_client: GremlinAPIHttpClient = get_gremlin_httpclient()
        t_uri: str = "test"
        self.assertEqual(f"{config.base_uri}{t_uri}", https_client.base_uri(t_uri))
