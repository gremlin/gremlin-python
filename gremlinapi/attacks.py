# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import json
import logging

from gremlinapi.exceptions import (
    GremlinParameterError,
    ProxyError,
    ClientError,
    HTTPTimeout,
    HTTPError
)

from gremlinapi.cli import register_cli_action
from gremlinapi.http_clients import get_gremlin_httpclient


log = logging.getLogger('GremlinAPI.client')


class GremlinAPIAttacks(object):


    @classmethod
    def _common_list_method(cls, https_client=get_gremlin_httpclient(), **kwargs):
        endpoint = kwargs.get('endpoint', None)
        if not endpoint:
            error_msg = f'endpoint not passed correctly: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        method = 'GET'
        headers = https_client.header()
        source = kwargs.get('source', None)
        page_size = kwargs.get('pageSize', None)
        team_id = kwargs.get('teamId', None)
        if source or page_size or team_id:
            endpoint += '/?'
            if source and (source.lower() == 'adhoc' or source.lower() == 'scenario'):
                endpoint += f'source={source}&'
            if page_size and isinstance(page_size, int):
                endpoint += f'pageSize={page_size}&'
            if team_id:
                endpoint += f'teamId={team_id}&'
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

    @classmethod
    @register_cli_action('create_attack', ('body',), ('teamId',))
    def create_attack(cls, https_client=get_gremlin_httpclient(), **kwargs):
        endpoint = '/attacks/new'

    @classmethod
    @register_cli_action('list_active_attacks', ('',), ('source', 'pageSize', 'teamId'))
    def list_active_attacks(cls, https_client=get_gremlin_httpclient(), **kwargs):
        """
        :param https_client:
        :param kwargs: { source(adhoc or scenario, query), pageSize(int32, query), teamId(string, query) }
        :return:
        """
        endpoint = '/attacks/active'
        kwargs['endpoint'] = endpoint
        return cls._common_list_method(https_client, kwargs)

    @classmethod
    @register_cli_action('list_attacks', ('',), ('source', 'pageSize', 'teamId'))
    def list_attacks(cls, https_client=get_gremlin_httpclient(), **kwargs):
        """
        :param https_client:
        :param kwargs: { source(adhoc or scenario, query), pageSize(int32, query), teamId(string, query) }
        :return:
        """
        endpoint = '/attacks'
        kwargs['endpoint'] = endpoint
        return cls._common_list_method(https_client, **kwargs)


    @classmethod
    @register_cli_action('list_complete_attacks', ('',), ('source', 'pageSize', 'teamId'))
    def list_completed_attacks(cls, https_client=get_gremlin_httpclient(), **kwargs):
        """
        :param https_client:
        :param kwargs: { source(adhoc or scenario, query), pageSize(int32, query), teamId(string, query) }
        :return:
        """
        endpoint = '/attacks/completed'
        kwargs['endpoint'] = endpoint
        return cls._common_list_method(https_client, **kwargs)

    @classmethod
    @register_cli_action('get_attack', ('guid',), ('teamId',))
    def get_attack(cls, https_client=get_gremlin_httpclient(), **kwargs):
        endpoint = '/attacks'
        method = 'GET'
        headers = https_client.header()
        guid = kwargs.get('guid', None)
        team_id = kwargs.get('teamId', None)
        if guid:
            endpoint += f'/{guid}'
        else:
            error_msg = f'Attack GUID was not passed: {kwargs}'
            log.critical(error_msg)
            raise GremlinParameterError(error_msg)
        if team_id:
            endpoint += '/?teamId={team_id};'
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

    @classmethod
    @register_cli_action('halt_all_attacks', ('',), ('teamId',))
    def halt_all_attacks(cls, https_client=get_gremlin_httpclient(), **kwargs):
        method = 'DELETE'
        endpoint = '/attacks'
        if 'teamId' in kwargs:
            endpoint += f'/?teamId={kwargs["teamId"]}'
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

    @classmethod
    @register_cli_action('halt_attack', ('guid',), ('teamId',))
    def halt_attack(cls, https_client=get_gremlin_httpclient(), **kwargs):
        method = 'DELETE'
        endpoint = '/attacks'
        if guid:
            endpoint += f'/{guid}'
        else:
            error_msg = f'Attack GUID was not passed: {kwargs}'
            log.critical(error_msg)
            raise GremlinParameterError(error_msg)
        if 'teamId' in kwargs:
            endpoint += f'/?teamId={kwargs["teamId"]}'
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

