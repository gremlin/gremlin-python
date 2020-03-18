# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging

from gremlinapi.cli import register_cli_action
from gremlinapi.exceptions import (
    GremlinParameterError,
    ProxyError,
    ClientError,
    HTTPTimeout,
    HTTPError
)

from gremlinapi.gremlinapi import GremlinAPI
from gremlinapi.http_clients import get_gremlin_httpclient


log = logging.getLogger('GremlinAPI.client')



class GremlinAPIHalts(GremlinAPI):

    @classmethod
    @register_cli_action('halt_all_attacks', ('',), ('teamId', 'body'))
    def halt_all_attacks(cls, https_client=get_gremlin_httpclient(), **kwargs):
        method = 'POST'
        data = kwargs.get('body', None)
        if not data:
            data = ''
        endpoint = cls._optional_team_endpoint('/halts', **kwargs)
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'body': data, 'headers': headers})
        return body

