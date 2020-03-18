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

    def __init__(self):
        pass

    @classmethod
    @register_cli_action('activate_client', ('guid',), ('teamId',))
    def activate_client(cls, https_client=get_gremlin_httpclient(), **kwargs):
        endpoint = '/clients'
        method = 'PUT'
        headers = https_client.header()
        guid = kwargs.get('guid', None)
        team_id = kwargs.get('teamId', None)
        if guid:
            endpoint += f'/{guid}/activate'
        else:
            error_msg = f'Client GUID was not passed: {kwargs}'
            log.critical(error_msg)
            raise GremlinParameterError(error_msg)
        if team_id:
            endpoint += '/?teamId={team_id};'
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

    @classmethod
    @register_cli_action('deactivate_client', ('guid',), ('teamId',))
    def deactivate_client(cls, https_client=get_gremlin_httpclient(), **kwargs):
        endpoint = '/clients'
        method = 'DELETE'
        headers = https_client.header()
        guid = kwargs.get('guid', None)
        team_id = kwargs.get('teamId', None)
        if guid:
            endpoint += f'/{guid}'
        else:
            error_msg = f'Client GUID was not passed: {kwargs}'
            log.critical(error_msg)
            raise GremlinParameterError(error_msg)
        if team_id:
            endpoint += '/?teamId={team_id};'
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

    @classmethod
    @register_cli_action('list_active_clients', ('',), ('teamId',))
    def list_active_clients(cls, https_client=get_gremlin_httpclient(), **kwargs):
        endpoint = '/clients/active'
        method = 'GET'
        headers = https_client.header()
        team_id = kwargs.get('teamId', None)
        if team_id:
            endpoint += '/?teamId={team_id};'
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

    @classmethod
    @register_cli_action('list_clients', ('',), ('teamId',))
    def list_clients(cls, https_client=get_gremlin_httpclient(), **kwargs):
        endpoint = '/clients'
        method = 'GET'
        headers = https_client.header()
        team_id = kwargs.get('teamId', None)
        if team_id:
            endpoint += '/?teamId={team_id};'
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body