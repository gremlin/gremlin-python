# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import json
import logging
import re

from gremlinapi.exceptions import (
    GremlinCommandTargetError,
    GremlinIdentifierError,
    GremlinParameterError
)

from gremlinapi.clients import GremlinAPIClients as clients
from gremlinapi.containers import GremlinAPIContainers as containers
from gremlinapi.providers import GremlinAPIProviders as providers

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
    def command(self, _command=None):
        if not issubclass(type(_command), GremlinAttackCommandHelper):
            error_msg = f'Command needs to be a child class of {type(GremlinAttackCommandHelper)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        if issubclass(type(_command), GremlinTimeTravelAttack) and \
                issubclass(type(self.target), GremlinTargetContainers):
            error_msg = f'TimeTravel cannot target containers'
            log.fatal(error_msg)
            raise GremlinCommandTargetError(error_msg)
        self._command = _command

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, _target=None):
        if not issubclass(type(_target), GremlinAttackTargetHelper):
            error_msg = f'Command needs to be a child class of {type(GremlinAttackTargetHelper)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        if issubclass(type(_target), GremlinTargetContainers) and \
                issubclass(type(self.command), GremlinTimeTravelAttack):
            error_msg = f'TimeTravel cannot target containers'
            log.fatal(error_msg)
            raise GremlinCommandTargetError(error_msg)
        self._target = _target

    def repr_model(self):
        model = {
            'target': json.loads(str(self.target)),
            'command': json.loads(str(self.command))
        }
        return model

    def __repr__(self):
        model = self.repr_model()
        return json.dumps(model)


class GremlinAttackTargetHelper(object):
    def __init__(self, *args, **kwargs):
        self._strategy_type = None
        self._exact = 0
        self._percent = 10
        self._allowed_strategy_types = {'exact': 'Exact', 'random': 'Random'}
        self.exact = kwargs.get('exact', self._exact)
        self.percent = kwargs.get('percent', self._percent)
        self.strategy_type = kwargs.get('strategy_type', 'random')  # Validate Random or Exact

    def target_definition(self):
        model = self.repr_model()
        _target_definition = {
            'strategyType': self.strategy_type,
            'strategy': dict()
        }
        if model.get('percent', None):
            _target_definition['strategy'] = {'percentage': model['percent']}
        elif model.get('exact', None):
            _target_definition['strategy'] = {'count': model['exact']}
        else:
            error_msg = 'Targeting was not properly defined'
            log.fatal(error_msg)
            raise GremlinCommandTargetError(error_msg)
        if type(model.get('containers')) == dict and model.get('containers').get('multiSelectLabels'):
            _target_definition['strategy']['multiSelectLabels'] = model['containers']['multiSelectLabels']
        if type(model.get('hosts')) == dict and model.get('hosts').get('multiSelectLabels'):
            _target_definition['strategy']['multiSelectLabels'] = model['hosts']['multiSelectLabels']
        return _target_definition

    def target_definition_graph(self):
        model = self.repr_model()
        _target_definition = {
            'strategy_type': self.strategy_type,
            'strategy': dict()
        }
        if model.get('percent', None):
            _target_definition['strategy'] = {'type': 'RandomPercent', 'percentage': model['percent']}
        elif model.get('exact', None):
            _target_definition['strategy'] = {'type': 'Exact', 'count': model['exact']}
        else:
            error_msg = 'Targeting was not properly defined'
            log.fatal(error_msg)
            raise GremlinCommandTargetError(error_msg)
        if type(model.get('containers')) == dict and model.get('containers').get('multiSelectLabels'):
            _target_definition['target_type'] = 'Container'
            _target_definition['strategy']['attrs'] = dict()
            _target_definition['strategy']['attrs']['multiSelectLabels'] = model['containers']['multiSelectLabels']
        if type(model.get('hosts')) == dict and model.get('hosts').get('multiSelectLabels'):
            _target_definition['target_type'] = 'Host'
            _target_definition['strategy']['attrs'] = dict()
            _target_definition['strategy']['attrs']['multiSelectLabels'] = model['hosts']['multiSelectLabels']
        return _target_definition

    @property
    def exact(self):
        return self._exact

    @exact.setter
    def exact(self, _exact=None):
        if not _exact:
            self._exact = 0
        elif isinstance(_exact, int) and _exact > 0:
            self._exact = _exact
            self._percent = 0
        else:
            error_msg = f'Exact number of targets must be an integer greater than 0'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)

    @property
    def percent(self):
        return self._percent

    @percent.setter
    def percent(self, _percent=None):
        if not _percent:
            self._percent = 0
        elif isinstance(_percent, int) and 1 <= _percent <= 100:
            self._percent = _percent
            self._exact = 0
        else:
            error_msg = f'Target percentage must be an integer between 1 and 100'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)

    @property
    def strategy_type(self):
        return self._strategy_type

    @strategy_type.setter
    def strategy_type(self, _target_type=None):
        if not isinstance(_target_type, str) or not self._allowed_strategy_types.get(_target_type.lower(), None):
            error_msg = f'strategy_type needs to be one of {str(self._allowed_strategy_types.keys())[1:-2]}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._strategy_type = self._allowed_strategy_types.get(_target_type.lower(), None)

    def repr_model(self):
        model = dict()
        model['type'] = self.strategy_type
        if self.exact >= 0 and not self.percent:
            model['exact'] = str(self.exact)
        elif self.strategy_type == 'Random':
            model['percent'] = self.percent
        else:
            error_msg = f'Type not correctly set, needs to be one of {str(self._allowed_strategy_types.keys())[1:-2]}'
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        return model

    def __repr__(self):
        model = self.repr_model()
        return json.dumps(model)


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

    # def target_definition(self):
    #     model = json.loads(self.__repr__())
    #     del model['type']
    #     _target_definition = super().target_definition()
    #     _target_definition['strategy'] = model
    #     _target_definition['targetType'] = 'Host'
    #     return _target_definition

    def target_definition(self):
        _target_definition = super().target_definition()
        _target_definition['targetType'] = 'Host'
        return _target_definition

    @property
    def ids(self):
        return self._ids

    @ids.setter
    def ids(self, _ids=None):
        if not isinstance(_ids, list):
            error_msg = f'ids expects a list of strings, received {type(_ids)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        for _identifier in _ids:
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
    def tags(self, _tags=None):
        if isinstance(_tags, dict):
            for _tag in _tags:
                if self._valid_tag_pair(_tag, _tags[_tag]):
                    self._multiSelectTags[_tag] = _tags[_tag]
        self._ids = []
        self.target_all_hosts = False

    @property
    def target_all_hosts(self):
        return self._target_all_hosts

    @target_all_hosts.setter
    def target_all_hosts(self, _target_all_hosts=False):
        if _target_all_hosts != False:
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

    def repr_model(self):
        model = super().repr_model()
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
        return model

    # def __repr__(self):
    #     model = json.loads(super().__repr__())
    #     if self.target_all_hosts:
    #         model['hosts'] = 'all'
    #     else:
    #         if len(self.ids) > 0:
    #             model['hosts'] = {
    #                 'ids': self.ids
    #             }
    #         elif len(self.tags) > 0:
    #             model['hosts'] = {
    #                 'multiSelectTags': self.tags
    #             }
    #     return json.dumps(model)


class GremlinTargetContainers(GremlinAttackTargetHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._active_containers = list()
        self._active_identifiers = list()
        self._active_labels = dict()
        self._ids = list()
        self._multiSelectLabels = dict()
        #self._nativeTags = {'os-type': 'os_type', 'os-version': 'os_version'}
        self._target_all_containers = True
        self.target_all_containers = kwargs.get('target_all_containers', True)
        self.ids = kwargs.get('ids', list())
        self.labels = kwargs.get('labels', dict())

    # def target_definition(self):
    #     model = json.loads(self.__repr__())
    #     del model['type']
    #     _target_definition = super().target_definition()
    #     _target_definition['strategy'] = {
    #         'percent': model['percent']
    #     }
    #     if model.get('multiSelectLabels'):
    #         _target_definition['strategy']['multiSelectLabels'] = model['multiSelectLabels']
    #     _target_definition['targetType'] = 'Container'
    #     return _target_definition

    def target_definition(self):
        _target_definition = super().target_definition()
        _target_definition['targetType'] = 'Container'
        return _target_definition

    @property
    def ids(self):
        return self._ids

    @ids.setter
    def ids(self, _ids=None):
        if not isinstance(_ids, list):
            error_msg = f'ids expects a list of strings, received {type(_ids)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        if len(_ids) >= 1:
            for _identifier in _ids:
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
            self._multiSelectLabels = {}
            self.target_all_containers = False

    @property
    def labels(self):
        return self._multiSelectLabels

    @labels.setter
    def labels(self, _labels=None):
        if not isinstance(_labels, dict):
            error_msg = f'labels expects a dictionary, received {type(_labels)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        if bool(_labels):
            for _label in _labels:
                if isinstance(_labels[_label], str):
                    if self._valid_label_pair(_label, _labels[_label]):
                        if isinstance(self._multiSelectLabels.get(_label, None), list):
                            self._multiSelectLabels[_label].append(_labels[_label])
                        else:
                            self._multiSelectLabels[_label] = [_labels[_label]]
                elif isinstance(_labels[_label], list()):
                    if not isinstance(self._multiSelectLabels[_label]):
                        self._multiSelectLabels[_label] = list()
                    for _value in _labels[_label]:
                        if self._valid_label_pair(_label, _value):
                            self._multiSelectLabels[_label].append(_value)

            self._ids = []
            self.target_all_containers = False

    @property
    def target_all_containers(self):
        return self._target_all_containers

    @target_all_containers.setter
    def target_all_containers(self, _target_all_containers=False):
        if _target_all_containers != False:
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

    def repr_model(self):
        model = super().repr_model()
        if self.target_all_containers:
            model['containers'] = 'all'
        else:
            if len(self.ids) > 0:
                model['containers'] = {
                    'ids': self.ids
                }
            elif len(self.labels) > 0:
                model['containers'] = {
                    'multiSelectLabels': self.labels
                }
        return model

    # def __repr__(self):
    #     model = json.loads(super().__repr__())
    #     if self.target_all_containers:
    #         model['containers'] = 'all'
    #     else:
    #         if len(self.ids) > 0:
    #             model['containers'] = {
    #                 'ids': self.ids
    #             }
    #         elif len(self.labels) > 0:
    #             model['containers'] = {
    #                 'multiSelectLabels': self.labels
    #             }
    #     return json.dumps(model)


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

    def impact_definition(self):
        model = self.repr_model()
        _impact_definition = {
            'commandArgs': {
                'cliArgs': [str(self.shortType)],
                'length': self.length
            },
            'commandType': str(self.shortType)
        }
        _impact_definition['commandArgs']['cliArgs'].extend(model['args'])
        return _impact_definition

    def impact_definition_graph(self):
        model = self.repr_model()
        _impact_definition = {
            'infra_command_args': {
                'cli_args': [str(self.shortType)],
                'type': str(self.shortType)
            },
            'infra_command_type': str(self.shortType)
        }
        _impact_definition['infra_command_args']['cli_args'].extend(model['args'])
        return _impact_definition

    @property
    def commandType(self):
        return self._commandType

    @commandType.setter
    def commandType(self, _commandType=None):
        if not isinstance(_commandType, str):
            error_msg = f'commandType expects a string, received {type(_commandType)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        try:
            self._shortType = list(self._typeMap.keys())[list(self._typeMap.values()).index(_commandType)]
        except ValueError:
            error_msg = f'commandType needs to be one of: {str(self._typeMap.values())[1:-2]}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._commandType = _commandType

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, _length=None):
        if not (isinstance(_length, int) and 1 <= _length <= 31449600):  # Roughly 1 year in seconds
            error_msg = f'Attack length needs to be an integer between 1 and 31449600'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._length = _length

    @property
    def shortType(self):
        return self._shortType

    @shortType.setter
    def shortType(self, _shortType=None):
        if not isinstance(_shortType, str):
            error_msg = f'type_ expects a string, received {type(_shortType)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        if not _shortType.lower() in self._typeMap:
            error_msg = f'invalid attack type, expected one of {str(self._typeMap.keys())[1:-2]}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._commandType = self._typeMap[_shortType]
        self._shortType = _shortType

    def repr_model(self):
        model = {
            'type': self.shortType,
            'commandType': self.commandType,
            'args': [
                '-l', str(self.length)
            ]
        }
        return model

    def __repr__(self):
        model = self.repr_model()
        return json.dumps(model)


class GremlinResourceAttackHelper(GremlinAttackCommandHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._blocksize = 4
        self._directory = '/tmp'
        self._percent = 100
        self._workers = 1

    @property
    def blocksize(self):
        return self._blocksize

    @blocksize.setter
    def blocksize(self, _blocksize=None):
        if not (isinstance(_blocksize, int) and _blocksize >= 1):
            error_msg = f'blocksize requires a positive integer'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._blocksize = _blocksize

    @property
    def directory(self):
        return self._directory

    @directory.setter
    def directory(self, _directory=None):
        if not isinstance(_directory, str):
            error_msg = f'directory requires a string, received {type(_directory)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._directory = _directory

    @property
    def percent(self):
        return self._percent

    @percent.setter
    def percent(self, _percent=None):
        if not (isinstance(_percent, int) and 1 <= _percent <= 100):
            error_msg = f'percent is required to be an int between 1 and 100'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._percent = _percent

    @property
    def workers(self):
        return self._workers

    @workers.setter
    def workers(self, _workers=None):
        if not (isinstance(_workers, int) and _workers >= 1):
            error_msg = 'workers requires a positive integer'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._workers = _workers


class GremlinStateAttackHelper(GremlinAttackCommandHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class GremlinNetworkAttackHelper(GremlinAttackCommandHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._allowed_protocols = ['ICMP', 'TCP', 'UDP']
        self._ips = list()
        self._hostnames = ['^api.gremlin.com']
        self._device = None
        self._egress_ports = ['^53']
        self._ingress_ports = list()
        self._port_regex = '([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])'
        self._port_validator = re.compile(f'^\^?{self._port_regex}(-{self._port_regex})?$')
        self._protocol = None
        self._providers = list()
        self._providers_filter = None
        self._source_ports = None
        self._tags = list()
        self._tags_filter = None
        self.device = kwargs.get('device', None)        # -d, str
        self.ips = kwargs.get('ips', None)              # -i, str
        self.protocol = kwargs.get('protocol', None)    # -P, str
        self.providers = kwargs.get('providers', None)  # providers block
        self.tags = kwargs.get('tags', None)            # tags block

    def _filter_providers(self):
        _providers = providers.list_providers()
        for _provider in _providers:
            self._providers_filter.extend(getattr(providers, f'list_{_provider}_services')())

    def _port_maker(self, _ports=None):
        port_list = list()
        if not _ports:
            pass
        elif isinstance(_ports, int) or isinstance(_ports, str):
            if self._validate_port_or_range(str(_ports)):
                port_list = [str(_ports)]
        elif isinstance(_ports, list):
            for _port in _ports:
                if self._validate_port_or_range(str(_port)):
                    port_list.append(str(_port))
        else:
            error_msg = f'_port_maker expects a {type(str)} or {type(int)} or a {type(list)} of the previous types'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        return port_list

    def _valid_tag_pair(self, tagKey=None, tagValue=None):
        return True

    def _validate_hostname(self, _hostname=None):
        return True

    def _validate_ip(self, _ip=None):
        return True

    def _validate_port_or_range(self, _port_or_range):
        if not self._port_validator.match(_port_or_range):
            error_msg = f'{_port_or_range} is not a valid port or port range'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        return True

    def _validate_provider(self, _provider=None):
        if not len(self._providers_filter) > 0:
            self._filter_providers()
        if _provider in self._providers_filter:
            return True
        return False

    @property
    def device(self):
        return self._device

    @device.setter
    def device(self, _device=None):
        if not _device:
            self._device = None
            return
        elif not isinstance(_device, str):
            error_msg = f'device expects type {type(str)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._device = _device

    @property
    def egress_ports(self):
        return self._egress_ports

    @egress_ports.setter
    def egress_ports(self, _egress_ports=None):
        self._egress_ports = self._port_maker(_egress_ports)

    @property
    def ingress_ports(self):
        return self._ingress_ports

    @ingress_ports.setter
    def ingress_ports(self, _ingress_ports=None):
        self._ingress_ports = self._port_maker(_ingress_ports)

    @property
    def ips(self):
        return self._ips

    @ips.setter
    def ips(self, _ips=None):
        if not _ips:
            pass
        elif isinstance(_ips, str):
            if self._validate_ip(_ips):
                pass
            self._ips = [_ips]
        elif isinstance(_ips, list):
            for _ip in _ips:
                if self._validate_ip(_ip):
                    pass
            self._ips = _ips
        else:
            error_msg = f'valid ip addresses required'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)

    @property
    def hostnames(self):
        return self._hostnames

    @hostnames.setter
    def hostnames(self, _hostnames=None):
        if not _hostnames:
            pass
        elif isinstance(_hostnames, str):
            if not self._validate_hostname(_hostnames):
                error_msg = f'valid hostnames required'
                log.fatal(error_msg)
                raise GremlinParameterError(error_msg)
            self._hostnames = [_hostnames]
        elif isinstance(_hostnames, list):
            for _hostname in _hostnames:
                if not self._validate_hostname(_hostname):
                    error_msg = f'valid hostnames required'
                    log.fatal(error_msg)
                    raise GremlinParameterError(error_msg)
                self._hostnames = _hostname
        else:
            error_msg = f'hostnames requires a {type(str)} or {type(list)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, _protocol=None):
        if not _protocol:
            self._protocol = None
            return
        elif not (isinstance(_protocol, str) and _protocol.upper() in self._allowed_protocols):
            error_msg = f'Protocol must be a string and one of {str(self._allowed_protocols)[1:-2]}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._protocol = _protocol.upper()

    @property
    def providers(self):
        return self._providers

    @providers.setter
    def providers(self, _providers=None):
        if not _providers:
            pass
        elif isinstance(_providers, str):
            if self._validate_provider(_providers):
                self._providers = [_providers]
        elif isinstance(_providers, list):
            self._providers = list()
            for _provider in _providers:
                if self._validate_provider(_provider):
                    self._providers.append(_provider)
        else:
            error_msg = f'providers expect a {type(str)} or {type(list)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)

    @property
    def source_ports(self):
        return self._source_ports

    @source_ports.setter
    def source_ports(self, _source_ports=None):
        self._source_ports = self._port_maker(_source_ports)

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, _tags=None):
        if isinstance(_tags, dict):
            for _tag in _tags:
                if self._valid_tag_pair(_tag, _tags[_tag]):
                    self._multiSelectTags[_tag] = _tags[_tag]
        self._ids = []
        self.target_all_hosts = False

    def repr_model(self):
        model = super().repr_model()
        if self.device:
            model['args'].extend(['-d', self.device])
        if len(self.ips) > 0:
            model['args'].extend(['-i', ','.join(self.ips)])
        if self.protocol:
            model['args'].extend(['-P', self.protocol])
        if self.providers and len(self.providers) > 0:
            model['providers'] = self.providers
        if self.tags and len(self.tags) > 0:
            model['trafficImpactMapping'] = {
                'multiSelectTags': self.tags
            }
        return model

    # def __repr__(self):
    #     model = json.loads(super().__repr__())
    #     if self.device:
    #         model['args'].extend(['-d', self.device])
    #     if len(self.ips) > 0:
    #         model['args'].extend(['-i', ','.join(self.ips)])
    #     if self.protocol:
    #         model['args'].extend(['-P', self.protocol])
    #     if self.providers and len(self.providers) > 0:
    #         model['providers'] = self.providers
    #     if self.tags and len(self.tags) > 0:
    #         model['trafficImpactMapping'] = {
    #             'multiSelectTags': self.tags
    #         }
    #     return json.dumps(model)


class GremlinCPUAttack(GremlinResourceAttackHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shortType = 'cpu'
        self._all_cores = False  # ['-a']
        self._capacity = 100  # ['-p', int]
        self._cores = 1  # ['-c', int]
        self.all_cores = kwargs.get('all_cores', False)  # -a
        self.capacity = kwargs.get('capacity', 100)      # -p, int
        self.cores = kwargs.get('cores', 1)              # -c, int

    @property
    def all_cores(self):
        return self._all_cores

    @all_cores.setter
    def all_cores(self, _all_cores=None):
        if not isinstance(_all_cores, bool):
            error_msg = f'all_cores expects a bool, received {type(_all_cores)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._all_cores = _all_cores

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, _capacity=None):
        if not (isinstance(_capacity, int) and 1 <= _capacity <= 100):
            error_msg = f'Capacity expects an integer between 1 and 100'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._capacity = _capacity

    @property
    def cores(self):
        return self._cores

    @cores.setter
    def cores(self, _cores=None):
        if not (isinstance(_cores, int) and _cores >= 1):
            error_msg = f'Cores expects a positive integer'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._cores = _cores

    def repr_model(self):
        model = super().repr_model()
        model['args'].extend(['-p', str(self.capacity)])
        if self.all_cores:
            model['args'].append('-a')
        else:
            model['args'].extend(['-c', str(self.cores)])
        return model

    # def __repr__(self):
    #     model = json.loads(super().__repr__())
    #     model['args'].extend(['-p', str(self.capacity)])
    #     if self.all_cores:
    #         model['args'].append('-a')
    #     else:
    #         model['args'].extend(['-c', str(self.cores)])
    #     return json.dumps(model)


class GremlinMemoryAttack(GremlinResourceAttackHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shortType = 'memory'
        self._allowedAmountTypes = ['MB', 'GB', '%']
        self._amount = '75'
        self._amountType = '%'
        self.amount = kwargs.get('amount', 100)          # ['-g' || '-m' || '-p'], int
        self.amountType = kwargs.get('amountType', '%')  # ['-g' || '-m' || '-p']

    # def impact_definition(self):
    #     model = json.loads(self.__repr__())
    #     _impact_definition = super().impact_definition()
    #     _impact_definition['commandArgs']['cliArgs'].extend(model['args'])
    #     return _impact_definition

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, _amount=None):
        if not (isinstance(_amount, int) and _amount >= 1):
            error_msg = f'amount expects a positive integer, received {type(_amount)}'
            log.fata(error_msg)
            raise GremlinParameterError(error_msg)
        if self.amountType == '%' and not 1 <= _amount <= 100:
            error_msg = f'amount must be an integer between 1 and 100 when amountType is set to %'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._amount = _amount

    @property
    def amountType(self):
        return self._amountType

    @amountType.setter
    def amountType(self, _amountType=None):
        if not (isinstance(_amountType, str) and _amountType.upper() in self._allowedAmountTypes):
            error_msg = f'amountType expects a string with a value belonging to {str(self._allowedAmountTypes)[1:-2]}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        if _amountType == '%' and not 1 <= self.amount <= 100:
            error_msg = f'amountType cannot be set to % while amount is not between 1 and 100'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._amountType = _amountType.upper()

    def repr_model(self):
        model = super().repr_model()
        if self.amountType == 'MB':
            model['args'].extend(['-m', str(self.amount)])
        elif self.amountType == 'GB':
            model['args'].extend(['-g', str(self.amount)])
        elif self.amountType == '%':
            model['args'].extend(['-p', str(self.amount)])
        else:
            error_msg = f'Fatal error, data model may be corrupted, amountType: {self._amountType} is not valid'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        return model

    # def __repr__(self):
    #     model = json.loads(super().__repr__())
    #     if self.amountType == 'MB':
    #         model['args'].extend(['-m', str(self.amount)])
    #     elif self.amountType == 'GB':
    #         model['args'].extend(['-g', str(self.amount)])
    #     elif self.amountType == '%':
    #         model['args'].extend(['-p', str(self.amount)])
    #     else:
    #         error_msg = f'Fatal error, repr_model model may be corrupted, amountType: {self._amountType} is not valid'
    #         log.fatal(error_msg)
    #         raise GremlinParameterError(error_msg)
    #     return json.dumps(model)


class GremlinDiskSpaceAttack(GremlinResourceAttackHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shortType = 'disk'
        self.blocksize = kwargs.get('blocksize', 4)
        self.directory = kwargs.get('directory', '/tmp')
        self.percent = kwargs.get('percent', 100)
        self.workers = kwargs.get('workers', 1)

    def repr_model(self):
        model = super().repr_model()
        model['args'].expand(['-d', str(self.directory)])
        model['args'].expand(['-w', str(self.workers)])
        model['args'].expand(['-b', str(self.blocksize)])
        model['args'].expand(['-p', str(self.percent)])
        return model

    # def __repr__(self):
    #     model = json.loads(super().__repr__())
    #     model['args'].expand(['-d', str(self.directory)])
    #     model['args'].expand(['-w', str(self.workers)])
    #     model['args'].expand(['-b', str(self.blocksize)])
    #     model['args'].expand(['-p', str(self.percent)])
    #     return json.dumps(model)


class GremlinDiskIOAttack(GremlinResourceAttackHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shortType = 'io'
        self._allowed_modes = ['r', 'rw', 'w']
        self._blockcount = 1
        self._mode = 'rw'
        self.blockcount = kwargs.get('blockcount', 1)     # -c, int
        self.blocksize = kwargs.get('blocksize', 4)       # -s, int
        self.directory = kwargs.get('directory', '/tmp')  # -d, str
        self.mode = kwargs.get('mode', 'rw')              # -m, str
        self.workers = kwargs.get('workers', 1)            # -w, int

    @property
    def blockcount(self):
        return self._blockcount

    @blockcount.setter
    def blockcount(self, _blockcount=None):
        if not (isinstance(_blockcount, int) and _blockcount >= 1):
            error_msg = f'blockcount requires a positive integer'
            log.debug(error_msg)
            raise GremlinParameterError(error_msg)
        self._blockcount = _blockcount

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, _mode=None):
        if not (isinstance(_mode, str) and _mode.lower() in self._allowed_modes):
            error_msg = f'mode needs to be one of {str(self._allowed_modes)[1:-2]}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._mode = _mode.lower()

    def repr_model(self):
        model = super().repr_model()
        model['args'].extend(['-c', str(self.blockcount)])
        model['args'].extend(['-d', self.directory])
        model['args'].extend(['-m', self.mode])
        model['args'].extend(['-s', str(self.blocksize)])
        model['args'].extend(['-w', str(self.workers)])
        return model

    # def __repr__(self):
    #     model = json.loads(super().__repr__())
    #     model['args'].extend(['-c', str(self.blockcount)])
    #     model['args'].extend(['-d', self.directory])
    #     model['args'].extend(['-m', self.mode])
    #     model['args'].extend(['-s', str(self.blocksize)])
    #     model['args'].extend(['-w', str(self.workers)])
    #     return json.dumps(model)


class GremlinShutdownAttack(GremlinStateAttackHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shortType = 'shutdown'
        self._delay = 1
        self._reboot = False
        self.delay = kwargs.get('delay', 1)        # -d, int
        self.reboot = kwargs.get('reboot', False)  # -r

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, _delay=None):
        if not (isinstance(_delay, int) and _delay >= 1):
            error_msg = f'delay expects a positive {type(int)}'
            log.fatal(error_msg)
            raise GremlinParameterError (error_msg)
        self._delay = _delay

    @property
    def reboot(self):
        return self._reboot

    @reboot.setter
    def reboot(self, _reboot=None):
        if not isinstance(_reboot, bool):
            error_msg = f'reboot expects a {type(bool)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._reboot = _reboot

    def repr_model(self):
        model = super().repr_model()
        model['args'] = ['-d', str(self.delay)]
        if self.reboot:
            model['args'].append('-r')
        return model

    # def __repr__(self):
    #     model = json.loads(super().__repr__())
    #     model['args'] = ['-d', str(self.delay)]
    #     if self.reboot:
    #         model['args'].append('-r')
    #     return json.dumps(model)


class GremlinProcessKillerAttack(GremlinStateAttackHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shortType = 'process_killer'
        self._exact = False
        self._full_match = False
        self._group = str()
        self._interval = 1
        self._kill_children = False
        self._process = str()
        self._target_newest = False
        self._target_oldest = False
        self._user = str()
        self.exact = kwargs.get('exact', False)                   # -e
        self.full_match = kwargs.get('full_match', False)         # -f
        self.group = kwargs.get('group', str())                   # -g, str
        self.interval = kwargs.get('interval', 1)                 # -i, int
        self.kill_children = kwargs.get('kill_children', False)   # -c
        self.process = kwargs.get('process', str())               # -p, str
        self.target_newest = kwargs.get('target_newest', False)   # -n
        self._target_oldest = kwargs.get('target_oldest', False)  # -o
        self.user = kwargs.get('user', str())                     # -p, str

    @property
    def exact(self):
        return self._exact

    @exact.setter
    def exact(self, _exact=None):
        if not isinstance(_exact, bool):
            error_msg = f'exact expects type {type(bool)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._exact = _exact

    @property
    def full_match(self):
        return self._full_match

    @full_match.setter
    def full_match(self, _full_match=None):
        if not _full_match:
            self._full_match = False
        elif not isinstance(_full_match, bool):
            error_msg = f'exact expects type {type(bool)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._full_match = True

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, _group=None):
        if not isinstance(_group, str):
            error_msg = f'group expects type {type(str)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._group = _group

    @property
    def interval(self):
        return self._interval

    @interval.setter
    def interval(self, _interval=None):
        if not (isinstance(_interval, int) and _interval >= 1):
            error_msg = f'group expects positive integer of type {type(int)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._interval = _interval

    @property
    def kill_children(self):
        return self._kill_children

    @kill_children.setter
    def kill_children(self, _kill_children=None):
        if not isinstance(_kill_children, bool):
            error_msg = f'kill_children expects {type(bool)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._kill_children = _kill_children

    @property
    def process(self):
        return self._process

    @process.setter
    def process(self, _process=None):
        if not isinstance(_process, str):
            error_msg = f'process expects {type(str)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._process = _process

    @property
    def target_newest(self):
        return self._target_newest

    @target_newest.setter
    def target_newest(self, _target_newest=None):
        if isinstance(_target_newest, bool):
            if _target_newest == True:
                self._target_newest = True
                self._target_oldest = False
            else:
                self._target_newest = False
        else:
            error_msg = f'target_newest expects type {type(bool)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)

    @property
    def target_oldest(self):
        return self._target_oldest

    @target_oldest.setter
    def target_oldest(self, _target_oldest=None):
        if isinstance(_target_oldest, bool):
            if _target_oldest == True:
                self._target_oldest = True
                self._target_newest = False
            else:
                self.target_oldest = False
        else:
            error_msg = f'target_oldest expects type {type(bool)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, _user=None):
        if not _user:
            self._user = None
        elif isinstance(_user, str):
            self._user = _user
        else:
            error_msg = f'user expects {type(str)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)

    def repr_model(self):
        model = super().repr_model()
        model['args'].extend(['-i', str(self.interval)])
        if self.group:
            model['args'].extend(['-g', self.group])
        if self.process:
            model['args'].extend(['-p', self.process])
        else:
            error_msg = f'process is required to a be a non-empty string'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        if self.user:
            model['args'].extend(['-u', self.user])
        if self.exact:
            model['args'].append('-e')
        if self.full_match:
            model['args'].append('-f')
        if self.kill_children:
            model['args'].append('-c')
        if self.target_newest and not self.target_oldest:
            model['args'].append('-n')
        if self.target_oldest and not self.target_newest:
            model['args'].append('-o')
        return model

    # def __repr__(self):
    #     model = json.loads(super().__repr__())
    #     model['args'].extend(['-i', str(self.interval)])
    #     if self.group:
    #         model['args'].extend(['-g', self.group])
    #     if self.process:
    #         model['args'].extend(['-p', self.process])
    #     else:
    #         error_msg = f'process is required to a be a non-empty string'
    #         log.fatal(error_msg)
    #         raise GremlinParameterError(error_msg)
    #     if self.user:
    #         model['args'].extend(['-u', self.user])
    #     if self.exact:
    #         model['args'].append('-e')
    #     if self.full_match:
    #         model['args'].append('-f')
    #     if self.kill_children:
    #         model['args'].append('-c')
    #     if self.target_newest and not self.target_oldest:
    #         model['args'].append('-n')
    #     if self.target_oldest and not self.target_newest:
    #         model['args'].append('-o')
    #     return json.dumps(model)


class GremlinTimeTravelAttack(GremlinStateAttackHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shortType = 'time_travel'
        self._block_ntp = False
        self._offset = 86400
        self.block_ntp = kwargs.get('block_ntp', False)  # -n
        self.offset = kwargs.get('offset', 86400)        # -o, int

    @property
    def block_ntp(self):
        return self._block_ntp

    @block_ntp.setter
    def block_ntp(self, _block_ntp=None):
        if not isinstance(_block_ntp, bool):
            error_msg = f'block_ntp expects type {type(bool)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._block_ntp = _block_ntp

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

    def repr_model(self):
        model = super().repr_model()
        model['args'].extend(['-o', str(self.offset)])
        if self.block_ntp:
            model['args'].append('-n')
        return model

    # def __repr__(self):
    #     model = json.loads(super().__repr__())
    #     model['args'].extend(['-o', str(self.offset)])
    #     if self.block_ntp:
    #         model['args'].append('-n')
    #     return json.dumps(model)


class GremlinBlackholeAttack(GremlinNetworkAttackHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shortType = 'blackhole'
        self.egress_ports = kwargs.get('egress_ports', ['^53'])       # -p, str
        self.hostnames = kwargs.get('hostnames', '^api.gremlin.com')  # -h, str
        self.ingress_ports = kwargs.get('ingress_ports', None)        # -n, str

    def repr_model(self):
        model = super().repr_model()
        if len(self.egress_ports) > 0:
            model['args'].extend(['-p', ','.join(self.egress_ports)])
        if len(self.hostnames) > 0:
            model['args'].extend(['-h', ','.join(self.hostnames)])
        if len(self.ingress_ports) > 0:
            model['args'].extend(['-n', ','.join(self.ingress_ports)])
        return model

    def __repr__(self):
        model = json.loads(super().__repr__())
        if len(self.egress_ports) > 0:
            model['args'].extend(['-p', ','.join(self.egress_ports)])
        if len(self.hostnames) > 0:
            model['args'].extend(['-h', ','.join(self.hostnames)])
        if len(self.ingress_ports) > 0:
            model['args'].extend(['-n', ','.join(self.ingress_ports)])
        return json.dumps(model)


class GremlinDNSAttack(GremlinNetworkAttackHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shortType = 'dns'
        self._allowed_protocols = ['TCP', 'UDP']
        self.protocol = kwargs.get('protocol', None)

    def repr_model(self):
        model = super().repr_model()
        return model

    # def __repr__(self):
    #     model = json.loads(super().__repr__())
    #     return json.dumps(model)


class GremlinLatencyAttack(GremlinNetworkAttackHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shortType = 'latency'
        self._delay = 100
        self.delay = kwargs.get('delay', 100)                         # -m, int
        self.egress_ports = kwargs.get('egress_ports', ['^53'])       # -p, str
        self.hostnames = kwargs.get('hostnames', '^api.gremlin.com')  # -h, str
        self.source_ports = kwargs.get('source_ports', None)          # -s, str

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, _delay=None):
        if not (isinstance(_delay, int) and _delay >= 1):
            error_msg = f'delay expects a positive integer type {type(int)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._delay = _delay

    def repr_model(self):
        model = super().repr_model()
        model['args'].extend(['-m', str(self.delay)])
        if len(self.egress_ports) > 0:
            model['args'].extend(['-p', ','.join(self.egress_ports)])
        if len(self.hostnames) > 0:
            model['args'].extend(['-h', ','.join(self.hostnames)])
        if len(self.source_ports) > 0:
            model['args'].extend(['-s', ','.join(self.source_ports)])
        return model

    # def __repr__(self):
    #     model = json.loads(super().__repr__())
    #     model['args'].extend(['-m', str(self.delay)])
    #     if len(self.egress_ports) > 0:
    #         model['args'].extend(['-p', ','.join(self.egress_ports)])
    #     if len(self.hostnames) > 0:
    #         model['args'].extend(['-h', ','.join(self.hostnames)])
    #     if len(self.source_ports) > 0:
    #         model['args'].extend(['-s', ','.join(self.source_ports)])
    #     return json.dumps(model)


class GremlinPacketLossAttack(GremlinNetworkAttackHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shortType = 'packet_loss'
        self._corrupt = False
        self._percent = 1
        self.corrupt = kwargs.get('corrupt', False)                   # -c
        self.egress_ports = kwargs.get('egress_ports', ['^53'])       # -p, str
        self.hostnames = kwargs.get('hostnames', '^api.gremlin.com')  # -h, str
        self.percent = kwargs.get('percent', 1)                       # -r, int
        self.source_ports = kwargs.get('source_ports', None)          # -s, str

    @property
    def corrupt(self):
        return self._corrupt

    @corrupt.setter
    def corrupt(self, _corrupt=None):
        if not _corrupt:
            self._corrupt = False
            return
        if not isinstance(_corrupt, bool):
            error_msg = f'corrupt expects type {type(bool)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._corrupt = _corrupt

    @property
    def percent(self):
        return self._percent

    @percent.setter
    def percent(self, _percent=None):
        if not (isinstance(_percent, int) and 1 <= _percent <= 100):
            error_msg = f'percent expects positive integer type {type(int)} between 1 and 100'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._percent = _percent

    def repr_model(self):
        model = super().repr_model()
        model['args'].extend(['-r', str(self.percent)])
        if len(self.egress_ports) > 0:
            model['args'].extend(['-p', ','.join(self.egress_ports)])
        if len(self.hostnames) > 0:
            model['args'].extend(['-h', ','.join(self.hostnames)])
        if len(self.source_ports) > 0:
            model['args'].extend(['-s', ','.join(self.source_ports)])
        if self.corrupt:
            model['args'].append('-c')
        return model

    # def __repr__(self):
    #     model = json.loads(super().__repr__())
    #     model['args'].extend(['-r', str(self.percent)])
    #     if len(self.egress_ports) > 0:
    #         model['args'].extend(['-p', ','.join(self.egress_ports)])
    #     if len(self.hostnames) > 0:
    #         model['args'].extend(['-h', ','.join(self.hostnames)])
    #     if len(self.source_ports) > 0:
    #         model['args'].extend(['-s', ','.join(self.source_ports)])
    #     if self.corrupt:
    #         model['args'].append('-c')
    #     return json.dumps(model)

