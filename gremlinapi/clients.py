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


class GremlinAPIClients(GremlinAPI):

    @classmethod
    @register_cli_action('activate_client', ('guid',), ('teamId',))
    def activate_client(cls, https_client=get_gremlin_httpclient(), **kwargs):
        method = 'PUT'
        guid = kwargs.get('guid', None)
        if not guid:
            error_msg = f'Client GUID was not passed: {kwargs}'
            log.critical(error_msg)
            raise GremlinParameterError(error_msg)
        endpoint = cls._optional_team_endpoint(f'/clients/{guid}/activate', **kwargs)
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

    @classmethod
    @register_cli_action('deactivate_client', ('guid',), ('teamId',))
    def deactivate_client(cls, https_client=get_gremlin_httpclient(), **kwargs):
        method = 'DELETE'
        guid = kwargs.get('guid', None)
        if not guid:
            error_msg = f'Client GUID was not passed: {kwargs}'
            log.critical(error_msg)
            raise GremlinParameterError(error_msg)
        endpoint = cls._optional_team_endpoint(f'/clients/{guid}', **kwargs)
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

    @classmethod
    @register_cli_action('list_active_clients', ('',), ('teamId',))
    def list_active_clients(cls, https_client=get_gremlin_httpclient(), **kwargs):
        method = 'GET'
        endpoint = cls._optional_team_endpoint(f'/clients/activate', **kwargs)
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

    @classmethod
    @register_cli_action('list_clients', ('',), ('teamId',))
    def list_clients(cls, https_client=get_gremlin_httpclient(), **kwargs):
        method = 'GET'
        endpoint = cls._optional_team_endpoint(f'/clients', **kwargs)
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body