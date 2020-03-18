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


class GremlinAPIScenarios(GremlinAPI):

    @classmethod
    @register_cli_action('list_scenarios', ('',), ('teamId',))
    def list_scenarios(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._optional_team_endpoint('/scenarios', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body


class GremlinAPIScenariosRecommended(GremlinAPI):
    pass