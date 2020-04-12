# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import json
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
from gremlinapi.attack_helpers import GremlinAttackHelper
from gremlinapi.http_clients import get_gremlin_httpclient


log = logging.getLogger('GremlinAPI.client')


class GremlinAPIAttacks(GremlinAPI):
    @classmethod
    def _list_endpoint(cls, endpoint, *args, **kwargs):
        if not endpoint:
            error_msg = f'endpoint not passed correctly: {args} :: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        source = cls._info_if_not_param('source', **kwargs)
        page_size = cls._info_if_not_param('pageSize', **kwargs)
        if source or page_size:
            endpoint += '/?'
            if source and (source.lower() == 'adhoc' or source.lower() == 'scenario'):
                endpoint += f'source={source}&'
            if page_size and isinstance(page_size, int):
                endpoint += f'pageSize={page_size}&'
        return cls._optional_team_endpoint(endpoint, **kwargs)

    @classmethod
    def _error_if_not_attack_body(cls, **kwargs):
        body = cls._error_if_not_param('body', **kwargs)
        if issubclass(type(body), GremlinAttackHelper):
            return str(body)
        else:
            error_msg = f'Body present but not of type {type(GremlinAttackHelper)}'
            log.warning(error_msg)
        return body

    @classmethod
    @register_cli_action('create_attack', ('body',), ('teamId',))
    def create_attack(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        data = cls._error_if_not_attack_body(**kwargs)
        endpoint = cls._optional_team_endpoint('/attacks/new', **kwargs)
        payload = cls._payload(**{'headers': https_client.header(), 'body': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('list_active_attacks', ('',), ('source', 'pageSize', 'teamId'))
    def list_active_attacks(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._list_endpoint('/attacks/active', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('list_attacks', ('',), ('source', 'pageSize', 'teamId'))
    def list_attacks(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        """
        :param https_client:
        :param kwargs: { source(adhoc or scenario, query), pageSize(int32, query), teamId(string, query) }
        :return:
        """
        method = 'GET'
        endpoint = cls._list_endpoint('/attacks', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body


    @classmethod
    @register_cli_action('list_complete_attacks', ('',), ('source', 'pageSize', 'teamId'))
    def list_completed_attacks(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        """
        :param https_client:
        :param kwargs: { source(adhoc or scenario, query), pageSize(int32, query), teamId(string, query) }
        :return:
        """
        method = 'GET'
        endpoint = cls._list_endpoint('/attacks/completed', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('get_attack', ('guid',), ('teamId',))
    def get_attack(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        guid = cls._error_if_not_param('guid', **kwargs)
        endpoint = cls._optional_team_endpoint(f'/attacks/{guid}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('halt_all_attacks', ('',), ('teamId',))
    def halt_all_attacks(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'DELETE'
        endpoint = cls._optional_team_endpoint('/attacks', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('halt_attack', ('guid',), ('teamId',))
    def halt_attack(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'DELETE'
        guid = cls._error_if_not_param('guid', **kwargs)
        endpoint = cls._optional_team_endpoint(f'/attacks/{guid}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

