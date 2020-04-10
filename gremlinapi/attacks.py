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


class GremlinAPIAttacks(GremlinAPI):
    @classmethod
    def _list_endpoint(cls, endpoint, *args, **kwargs):
        if not endpoint:
            error_msg = f'endpoint not passed correctly: {args} :: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        source = cls._warn_if_not_param('source', **kwargs)
        page_size = cls._warn_if_not_param('pageSize', **kwargs)
        if source or page_size:
            endpoint += '/?'
            if source and (source.lower() == 'adhoc' or source.lower() == 'scenario'):
                endpoint += f'source={source}&'
            if page_size and isinstance(page_size, int):
                endpoint += f'pageSize={page_size}&'
        return cls._optional_team_endpoint(endpoint, **kwargs)

    @classmethod
    @register_cli_action('create_attack', ('body',), ('teamId',))
    def create_attack(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        data = cls._error_if_not_json_body(**kwargs)
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


class GremlinTargetHelper:
    def __init__(self, *args, **kwargs):
        self._target_type = kwargs.get('targetType', 'Random')  # Validate Random or Exact
        self._target_model = {
            'type': 'Random',  # Random or Exact
            'hosts': {  # could also just be 'all' instead of dictionary
                'ids': ['list', 'of', 'hosts'],
                'multiSelectTags': {  # Exclusive of ids
                    'os-type': ['Linux'],
                    'zone': ['us-east-1a'],
                    'region': ['us-east-1'],
                    'local-hostname': ['list', 'of', 'internal', 'hostnames'],
                    'local-ip': ['list', 'of', 'ip addresses'],
                    'public-hostname': ['list', 'of', 'external', 'hostname'],
                    'any-tag': ['any', 'list', 'of', 'values']
                }
            },
            'containers': {  # could also just be 'all'
                'ids': ['list', 'of', 'container', 'ids'],
                'multiSelectLabels': {
                    'any-label': ['any', 'list', 'of', 'values']
                }
            },
            'percent': 100,  # Integer, only used with type: random
            'exact': 1  # Exclusive to percent, used to target X hosts
        }

class GremlinTargetHosts(GremlinTargetHelper):
    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)
        self._target_model = {
            'type': 'Random',  # Random or Exact
            'hosts': {  # could also just be 'all' instead of dictionary
                'ids': ['list', 'of', 'hosts'],
                'multiSelectTags': {  # Exclusive of ids
                    'os-type': ['Linux'],
                    'zone': ['us-east-1a'],
                    'region': ['us-east-1'],
                    'local-hostname': ['list', 'of', 'internal', 'hostnames'],
                    'local-ip': ['list', 'of', 'ip addresses'],
                    'public-hostname': ['list', 'of', 'external', 'hostname'],
                    'any-tag': ['any', 'list', 'of', 'values']
                }
            },
            'percent': 100,  # Integer, only used with type: random
            'exact': 1  # Exclusive to percent, used to target X hosts
        }


class GremlinTargetContainers(GremlinTargetHelper):
    def __init__(self, *args, **kwargs):
        super.__init__(*args, **kwargs)
        self._target_model = {
            'type': 'Random',  # Random or Exact
            'containers': {  # could also just be 'all'
                'ids': ['list', 'of', 'container', 'ids'],
                'multiSelectLabels': {
                    'any-label': ['any', 'list', 'of', 'values']
                }
            },
            'percent': 100,  # Integer, only used with type: random
            'exact': 1  # Exclusive to percent, used to target X hosts
        }


class GremlinAttackHelper:
    def __init__(self, *args, **kwargs):
        self._target_type = kwargs.get('targetType', 'Random')  # Validate Random or Exact


class GremlinResourceAttackHelper(GremlinAttackHelper):
    def __init__(self):
        super.__init__()


class GremlinStateAttackHelper(GremlinAttackHelper):
    def __init__(self):
        super.__init__()


class GremlinNetworkAttackHelper(GremlinAttackHelper):
    def __init__(self):
        super.__init__()



class GremlinCPUAttack(GremlinResourceAttackHelper):
    def __init__(self):
        pass


class GremlinMemoryAttack(GremlinResourceAttackHelper):
    def __init__(self):
        pass


class GremlinDiskSpaceAttack(GremlinResourceAttackHelper):
    def __init__(self):
        pass


class GremlinDiskIOAttack(GremlinResourceAttackHelper):
    def __init__(self):
        pass


class GremlinShutdownAttack(GremlinStateAttackHelper):
    def __init__(self):
        pass


class GremlinProcessKillerAttack(GremlinStateAttackHelper):
    def __init__(self):
        pass


class GremlinTimeTravelAttack(GremlinStateAttackHelper):
    def __init__(self):
        pass


class GremlinBlackholeAttack(GremlinNetworkAttackHelper):
    def __init__(self):
        pass


class GremlinDNSAttack(GremlinNetworkAttackHelper):
    def __init__(self):
        pass


class GremlinLatencyAttack(GremlinNetworkAttackHelper):
    def __init__(self):
        pass


class GremlinPacketLossAttack(GremlinNetworkAttackHelper):
    def __init__(self):
        pass
