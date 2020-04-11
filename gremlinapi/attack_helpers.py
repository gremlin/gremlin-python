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


class GremlinAttackHelper(object):
    def __init__(self, *args, **kwargs):
        self._command = None
        self._target = None
        self.command = kwargs.get('command', GremlinCPUAttack())
        self.target = kwargs.get('target', GremlinTargetHosts())

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, command=None):
        if not issubclass(type(command), GremlinAttackCommandHelper):
            error_msg = f'Command needs to be a child class of {type(GremlinAttackCommandHelper)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._command = command

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, target=None):
        if not issubclass(type(target), GremlinAttackTargetHelper):
            error_msg = f'Command needs to be a child class of {type(GremlinAttackTargetHelper)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._target = target

    def __repr__(self):
        model = {
            'target': json.loads(str(self.target)),
            'command': json.loads(str(self.command))
        }
        return json.dumps(model)


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
        self._active_containers = list()
        self._active_identifiers = list()
        self._active_labels = dict()
        self._ids = list()
        self._multiSelectTags = dict()
        #self._nativeTags = {'os-type': 'os_type', 'os-version': 'os_version'}
        self._target_all_containers = True
        self.target_all_containers = kwargs.get('target_all_containers', True)
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
        self.target_all_containers = False

    @property
    def labels(self):
        return self._multiSelectTags

    @labels.setter
    def labels(self, labels=None):
        if isinstance(labels, dict):
            for _label in labels:
                if self._valid_label_pair(_label, labels[_label]):
                    self._multiSelectTags[_label] = labels[_label]
        self._ids = []
        self.target_all_containers = False

    @property
    def target_all_containers(self):
        return self._target_all_containers

    @target_all_containers.setter
    def target_all_containers(self, targetAllContainers=False):
        if targetAllContainers != False:
            self._target_all_containers = True
        else:
            self._target_all_containers = False

    def _filter_active_identifiers(self):
        if not len(self._active_identifiers) > 0:
            self._load_active_containers()
            for _container in self._active_containers:
                self._active_identifiers.append(_container['identifier'])

    def _filter_active_labels(self):
        if not len(self._active_labels) > 0:
            self._load_active_containers()
            for _container in self._active_containers:
                for _label in _container.get('container_labels'):
                    if not self._active_labels.get(_label):
                        self._active_labels[_label] = list()
                    _label_value = _container['container_labels'].get(_label)
                    if isinstance(_label_value, str):
                        if _label_value not in self._active_labels[_label]:
                            self._active_labels[_label].append(_label_value)
                    elif isinstance(_label_value, list):
                        for _inner_label_value in _container['container_labels'].get(_label):
                            if _inner_label_value not in self._active_labels[_label]:
                                self._active_labels[_label].append(_inner_label_value)

    def _load_active_containers(self):
        if not len(self._active_containers) > 0:
            self._active_containers = containers.list_containers()

    def _valid_identifier(self, identifier=None):
        if not self._active_identifiers:
            self._filter_active_identifiers()
        if identifier in self._active_identifiers:
            return True
        return False

    def _valid_label_pair(self, labelKey=None, labelValue=None):
        if not self._active_labels:
            self._filter_active_labels()
        if labelValue in self._active_labels.get(labelKey, []):
            return True
        return False

    def __repr__(self):
        model = json.loads(super().__repr__())
        if self.target_all_containers:
            model['containers'] = 'all'
        else:
            if len(self.ids) > 0:
                model['containers'] = {
                    'ids': self.ids
                }
            elif len(self.labels) > 0:
                model['containers'] = {
                    'multiSelectTags': self.labels
                }
        return json.dumps(model)

class GremlinAttackCommandHelper(object):
    def __init__(self, *args, **kwargs):
        self._length = 60
        self._commandType = str()
        self._shortType = str()
        self._typeMap = {
            'cpu': 'CPU',
            'memory': 'Memory',
            'disk': 'Disk',
            'io': 'IO',
            'process_killer': 'Process Killer',
            'shutdown': 'Shutdown',
            'time_travel': 'Time Travel',
            'blackhole': 'Blackhole',
            'dns': 'DNS',
            'latency': 'Latency',
            'packet_loss': 'Packet Loss'
        }
        self.length = kwargs.get('length', 60)

    @property
    def commandType(self):
        return self._commandType

    @commandType.setter
    def commandType(self, commandType=None):
        if not isinstance(commandType, str):
            error_msg = f'commandType expects a string, received {type(commandType)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        try:
            self._shortType = list(self._typeMap.keys())[list(self._typeMap.values()).index(commandType)]
        except ValueError:
            error_msg = f'commandType needs to be one of: {str(self._typeMap.values())[1:-2]}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._commandType = commandType

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length):
        if not (isinstance(length, int) and 60 <= length <= 31449600):  # Roughly 1 year in seconds
            error_msg = f'Attack length needs to be an integer between 60 and 31449600'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._length = length

    @property
    def shortType(self):
        return self._shortType

    @shortType.setter
    def shortType(self, shortType=None):
        if not isInstance(shortType, str):
            error_msg = f'type_ expects a string, received {type(shortType)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        if not shortType.lower() in self._typeMap:
            error_msg = f'invalid attack type, expected one of {str(self._typeMap.keys())[1:-2]}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._commandType = self._typeMap[shortType]
        self._shortType = shortType

    def __repr__(self):
        model = {
            'type': self.shortType,
            'commandType': self.commandType,
            'args': [
                '-l', self.length
            ]
        }
        return json.dumps(model)


class GremlinResourceAttackHelper(GremlinAttackCommandHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        model = json.loads(super().__repr__())
        return json.dumps(model)


class GremlinStateAttackHelper(GremlinAttackCommandHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        model = json.loads(super().__repr__())
        return json.dumps(model)


class GremlinNetworkAttackHelper(GremlinAttackCommandHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._allowed_protocols = ['ICMP', 'TCP', 'UDP']
        self._ips = list()
        self._hostnames = ['^api.gremlin.com']
        self._devices = list()
        self._egress_ports = list()
        self._ingress_ports = list()
        self._protocol = str()
        self._providers = list()
        self._tags = list()


    @property
    def egress_ports(self):
        return self._egress_ports

    @egress_ports.setter
    def egress_ports(self, egressPorts=None):
        pass

    @property
    def protocol(self):
        # -P [TCP, UDP, ICMP]
        return self._protocol

    @protocol.setter
    def protocol(self, protocol=None):
        if not (isinstance(protocol, str) and protocol.upper() in self._allowed_protocols):
            error_msg = f'Protocol must be a string and one of {str(self._allowed_protocols)[1:-2]}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._protocol = protocol.upper()

    @property
    def providers(self):
        return self._providers

    @property
    def source_ports(self):
        pass

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, tags=None):
        model = {
            'trafficImpactMapping': {
                'multiSelectTags': {
                    'tagName': ['list', 'tag', 'values']
                }
            }
        }
        pass

    def __repr__(self):
        model = json.loads(super().__repr__())
        return json.dumps(model)


class GremlinCPUAttack(GremlinResourceAttackHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shortType = 'cpu'
        self._capacity = 100  # ['-p', int]
        self._cores = 1  # ['-c', int]
        self._all_cores = False  # ['-a']


    def __repr__(self):
        model = json.loads(super().__repr__())
        return json.dumps(model)


class GremlinMemoryAttack(GremlinResourceAttackHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shortType = 'memory'

    def __repr__(self):
        model = json.loads(super().__repr__())
        return json.dumps(model)


class GremlinDiskSpaceAttack(GremlinResourceAttackHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shortType = 'disk'

    def __repr__(self):
        model = json.loads(super().__repr__())
        return json.dumps(model)


class GremlinDiskIOAttack(GremlinResourceAttackHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shortType = 'io'

    def __repr__(self):
        model = json.loads(super().__repr__())
        return json.dumps(model)


class GremlinShutdownAttack(GremlinStateAttackHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shortType = 'shutdown'

    def __repr__(self):
        model = json.loads(super().__repr__())
        return json.dumps(model)


class GremlinProcessKillerAttack(GremlinStateAttackHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shortType = 'process_killer'

    def __repr__(self):
        model = json.loads(super().__repr__())
        return json.dumps(model)

class GremlinTimeTravelAttack(GremlinStateAttackHelper):
    def __init__(self, *arge, **kwargs):
        super().__init__(*args, **kwargs)
        self.shortType = 'time_travel'
        self._offset = 86400
        self._blockNTP = False

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset=None):
        if not isinstance(offset, int):
            error_msg = f'Offset needs to be an integer, received {type(offset)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._offset = offset

    def __repr__(self):
        model = json.loads(super().__repr__())
        return json.dumps(model)


class GremlinBlackholeAttack(GremlinNetworkAttackHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shortType = 'blackhole'

    def __repr__(self):
        model = json.loads(super().__repr__())
        return json.dumps(model)


class GremlinDNSAttack(GremlinNetworkAttackHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shortType = 'dns'

    def __repr__(self):
        model = json.loads(super().__repr__())
        return json.dumps(model)


class GremlinLatencyAttack(GremlinNetworkAttackHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shortType = 'latency'

    def __repr__(self):
        model = json.loads(super().__repr__())
        return json.dumps(model)


class GremlinPacketLossAttack(GremlinNetworkAttackHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shortType = 'packet_loss'

    @property
    def corrupt(self):
        # args: [ '-c' ]
        pass

    def __repr__(self):
        model = json.loads(super().__repr__())
        return json.dumps(model)

