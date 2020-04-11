# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import json
import logging

from gremlinapi.exceptions import (
    GremlinIdentifierError,
    GremlinParameterError
)

from gremlinapi.attacks import GremlinAPIAttacks as attacks
from gremlinapi.clients import GremlinAPIClients as clients
from gremlinapi.containers import GremlinAPIContainers as containers


log = logging.getLogger('GremlinAPI.client')


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
        self._active_clients = list()
        self._active_identifiers = list()
        self._active_tags = dict()
        self._ids = list()
        self._multiSelectTags = dict()
        self._nativeTags = {'os-type': 'os_type', 'os-version': 'os_version'}
        self._target_all_hosts = False
        self.target_all_hosts = kwargs.get('target_all_hosts', True)

    @property
    def ids(self):
        return self._ids

    @ids.setter
    def ids(self, identifiers=None):
        if not isinstance(identifiers, list):
            error_msg = f'ids expects a list of strings, received {type(identifiers)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        for _identifier in identifiers:
            if not isinstance(_identifier, str):
                error_msg = f'Identifier not string; ids expect a string or list of strings'
                log.fatal(error_msg)
                raise GremlinParameterError(error_msg)
            if self._valid_identifier(_identifier):
                self._ids.append(_identifier)
            else:
                error_msg = f'Target identifier "{_identifier}" not found in active clients'
                log.warning(error_msg)
                raise GremlinIdentifierError(error_msg)
        self._multiSelectTags = {}
        self.target_all_hosts = False

    @property
    def tags(self):
        return self._multiSelectTags

    @tags.setter
    def tags(self, tags=None):
        if isinstance(tags, dict):
            for _tag in tags:
                if self._valid_tag_pair(_tag, tags[_tag]):
                    self._multiSelectTags[_tag] = tags[_tag]
        self._ids = []
        self.target_all_hosts = False

    @property
    def target_all_hosts(self):
        return self._target_all_hosts

    @target_all_hosts.setter
    def target_all_hosts(self, targetAllHosts=False):
        if targetAllHosts != False:
            self._target_all_hosts = True
        else:
            self._target_all_hosts = False

    def _filter_active_identifiers(self):
        if not len(self._active_identifiers) > 0:
            self._load_active_clients()
            for _client in self._active_clients:
                self._active_identifiers.append(_client['identifier'])

    def _filter_active_tags(self):
        if not len(self._active_tags) > 0:
            self._load_active_clients()
            for _client in self._active_clients:
                for _tag in self._nativeTags:
                    if not self._active_tags.get(_tag):
                        self._active_tags[_tag] = list()
                    if _client.get(_tag) not in self._active_tags[_tag]:
                        self._active_tags[_tag].append(_client.get(_tag))
                for _tag in _client.get('tags'):
                    if not self._active_tags.get(_tag):
                        self._active_tags[_tag] = list()
                    _tag_value = _client['tags'].get(_tag)
                    if isinstance(_tag_value, str):
                        if _tag_value not in self._active_tags[_tag]:
                            self._active_tags[_tag].append(_tag_value)
                    elif isinstance(_tag_value, list):
                        for _inner_tag_value in _client['tags'].get(_tag):
                            if _inner_tag_value not in self._active_tags[_tag]:
                                self._active_tags[_tag].append(_inner_tag_value)

    def _load_active_clients(self):
        if not len(self._active_clients) > 0:
            self._active_clients = clients.list_active_clients()

    def _valid_identifier(self, identifier=None):
        if not self._active_identifiers:
            self._filter_active_identifiers()
        if identifier in self._active_identifiers:
            return True
        return False

    def _valid_tag_pair(self, tagKey=None, tagValue=None):
        if not self._active_tags:
            self._filter_active_tags()
        if tagValue in self._active_tags.get(tagKey, []):
            return True
        return False

    def __repr__(self):
        model = json.loads(super().__repr__())
        if self.target_all_hosts:
            model['hosts'] = 'all'
        else:
            if len(self.ids) > 0:
                model['hosts'] = {
                    'ids': self.ids
                }
            elif len(self.tags) > 0:
                model['hosts'] = {
                    'multiSelectTags': self.tags
                }
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

