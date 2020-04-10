# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import json
import logging

from gremlinapi.exceptions import (
    GremlinParameterError
)

from gremlinapi.gremlinapi import GremlinAPI
from gremlinapi.attacks import GremlinAPIAttacks as attacks
from gremlinapi.clients import GremlinAPIClients as clients


class GremlinAttackTargetHelper(object):
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
        if self.target_type == 'Exact':
            model['exact'] = self.exact
        elif self.target_type == 'Random':
            model['percent'] = self.percent
        else:
            error_msg = f'Type not correctly set, needs to be one of {str(self._allowed_target_types.keys())[1:-2]}'
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        return json.dumps(model)

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
        super().__init__(*args, **kwargs)
        self._target_model = {
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
            }
        }

    def __repr__(self):
        model = json.loads(super().__repr__())
        model['hosts'] = dict()
        return json.dumps(model)


class GremlinTargetContainers(GremlinAttackTargetHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._target_model = {
            'containers': {  # could also just be 'all'
                'ids': ['list', 'of', 'container', 'ids'],
                'multiSelectLabels': {
                    'any-label': ['any', 'list', 'of', 'values']
                }
            },
            'percent': 100,  # Integer, only used with type: random
            'exact': 1  # Exclusive to percent, used to target X hosts
        }


class GremlinAttackCommandHelper(object):
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
    def __init__(self, *arge, **kwargs):
        super().__init__(*args, **kwargs)


class GremlinStateAttackHelper(GremlinAttackCommandHelper):
    def __init__(self, *arge, **kwargs):
        super().__init__(*args, **kwargs)


class GremlinNetworkAttackHelper(GremlinAttackCommandHelper):
    def __init__(self, *arge, **kwargs):
        super().__init__(*args, **kwargs)

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
    def __init__(self, *arge, **kwargs):
        super().__init__(*args, **kwargs)


class GremlinMemoryAttack(GremlinResourceAttackHelper):
    def __init__(self, *arge, **kwargs):
        super().__init__(*args, **kwargs)


class GremlinDiskSpaceAttack(GremlinResourceAttackHelper):
    def __init__(self, *arge, **kwargs):
        super().__init__(*args, **kwargs)


class GremlinDiskIOAttack(GremlinResourceAttackHelper):
    def __init__(self, *arge, **kwargs):
        super().__init__(*args, **kwargs)


class GremlinShutdownAttack(GremlinStateAttackHelper):
    def __init__(self, *arge, **kwargs):
        super().__init__(*args, **kwargs)


class GremlinProcessKillerAttack(GremlinStateAttackHelper):
    def __init__(self, *arge, **kwargs):
        super().__init__(*args, **kwargs)


class GremlinTimeTravelAttack(GremlinStateAttackHelper):
    def __init__(self, *arge, **kwargs):
        super().__init__(*args, **kwargs)


class GremlinBlackholeAttack(GremlinNetworkAttackHelper):
    def __init__(self, *arge, **kwargs):
        super().__init__(*args, **kwargs)


class GremlinDNSAttack(GremlinNetworkAttackHelper):
    def __init__(self, *arge, **kwargs):
        super().__init__(*args, **kwargs)


class GremlinLatencyAttack(GremlinNetworkAttackHelper):
    def __init__(self, *arge, **kwargs):
        super().__init__(*args, **kwargs)


class GremlinPacketLossAttack(GremlinNetworkAttackHelper):
    def __init__(self, *arge, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def corrupt(cls, *args, **kwargs):
        # args: [ '-c' ]
        pass

