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


class GremlinAttackTargetHelper:
    def __init__(self, *args, **kwargs):
        self._target_type = None
        self._exact = None
        self._percent = None
        self._allowed_target_types = {'exact': 'Exact', 'random': 'Random'}
        self.exact = kwargs.get('exact', 1)
        self.percent = kwargs.get('percent', 1)
        self.target_type = kwargs.get('target_type', 'random')  # Validate Random or Exact

    def __repr__(self):
        model = dict()
        model['type'] = self.target_type
        if self.target_type is 'Exact':
            model['exact'] = self.exact
        elif self.target_type is 'Random':
            model['percent'] = self.percent
        else:
            error_msg = f'Type not correctly set, needs to be one of {str(self._allowed_target_types.keys())[1:-2]}'
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        return model

    @property
    def exact(self):
        return self._exact

    @exact.setter
    def exact(self, exactTargets=None):
        if not isinstance(exactTargets, int) and exactTargets > 0:
            error_msg = f'Exact number of targets must be an integer greater than 0'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._exact = exactTargets

    @property
    def percent(self):
        return self._percent

    @percent.setter
    def percent(self, percentTargets=None):
        if not isinstance(percentTargets, int) and 1 <= percentTargets <= 100:
            error_msg = f'Target percentage must be an integer between 1 and 100'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._percent = percentTargets

    @property
    def target_type(self):
        return self._target_type

    @target_type.setter
    def target_type(self, targetType=None):
        if not isinstance(targetType, str) or not self._allowed_target_types.get(targetType.lower(), None):
            error_msg = f'target_type needs to be one of {str(self._allowed_target_types.keys())[1:-2]}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._target_type = self._allowed_target_types.get(targetType.lower(), None)


class GremlinTargetHosts(GremlinAttackTargetHelper):
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


class GremlinTargetContainers(GremlinAttackTargetHelper):
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


class GremlinAttackCommandHelper:
    def __init__(self, *args, **kwargs):
        self._target_type = kwargs.get('targetType', 'Random')  # Validate Random or Exact
        self._command_model = {
            'type': 'command-type',  # 'packet_loss'
            'commandType': 'Command Type',  # 'Packet Loss'
            'args': [
                '-l', '60'
            ],
            'providers': []
        }

    @classmethod
    def length(cls, *args, **kwargs):
        pass


class GremlinResourceAttackHelper(GremlinAttackCommandHelper):
    def __init__(self):
        super.__init__()


class GremlinStateAttackHelper(GremlinAttackCommandHelper):
    def __init__(self):
        super.__init__()


class GremlinNetworkAttackHelper(GremlinAttackCommandHelper):
    def __init__(self):
        super.__init__()

    @classmethod
    def blacklist_host(cls, *args, **kwargs):
        pass

    @classmethod
    def egress_ports(cls, *args, **kwargs):
        pass

    @classmethod
    def protocol(cls, *args, **kwargs):
        # -P [TCP, UDP, ICMP]
        pass

    @classmethod
    def providers(cls, *args, **kwargs):
        pass

    @classmethod
    def source_ports(cls, *args, **kwargs):
        pass

    @classmethod
    def tags(cls, *args, **kwargs):
        model = {
            'trafficImpactMapping': {
                'multiSelectTags': {
                   'tagName': ['list', 'tag', 'values']
                }
            }
        }
        pass

    @classmethod
    def whitelist_host(cls, *args, **kwargs):
        pass









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

    @classmethod
    def corrupt(cls, *args, **kwargs):
        # args: [ '-c' ]
        pass

