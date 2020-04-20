# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging

from gremlinapi.cli import register_cli_action
from gremlinapi.exceptions import (
    GremlinParameterError,
    ClientError,
    HTTPTimeout,
    HTTPError
)

from gremlinapi.gremlinapi import GremlinAPI
from gremlinapi.http_clients import get_gremlin_httpclient


log = logging.getLogger('GremlinAPI.client')


class GremlinAPIapikeys(GremlinAPI):
    @classmethod
    @register_cli_action('create_apikey', ('description', 'identifier',), ('teamId',))
    def create_apikey(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        data = {'description': cls._error_if_not_param('description', **kwargs),
                'identifier': cls._error_if_not_param('identifier', **kwargs)}
        endpoint = cls._optional_team_endpoint(f'/apikeys', **kwargs)
        payload = cls._payload(**{'headers': https_client.header(), 'body': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body


    @classmethod
    @register_cli_action('list_apikeys', ('',), ('teamId',))
    def list_apikeys(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._optional_team_endpoint(f'/apikeys', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('revoke_apikey', ('identifier',), ('teamId',))
    def revoke_apikey(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'DELETE'
        identifier = cls._error_if_not_param('identifier', **kwargs)
        endpoint = cls._optional_team_endpoint(f'/apikeys/{identifier}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body