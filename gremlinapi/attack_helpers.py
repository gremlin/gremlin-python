# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import json
import logging
import re

from gremlinapi.exceptions import (
    GremlinCommandTargetError,
    GremlinIdentifierError,
    GremlinParameterError,
)

from typing import Type, Optional, Union, Dict, TypedDict, Any, Pattern

from gremlinapi.clients import GremlinAPIClients as clients
from gremlinapi.containers import GremlinAPIContainers as containers
from gremlinapi.providers import GremlinAPIProviders as providers

log = logging.getLogger("GremlinAPI.client")


class GremlinAttackTargetHelper(object):
    def __init__(self, *args: tuple, **kwargs: dict):
        self._strategy_type: str = ""
        self._exact: int = 0
        self._percent: int = 10
        self._allowed_strategy_types: dict = {"exact": "Exact", "random": "Random"}
        self.exact = kwargs.get("exact", self._exact)  # type: ignore
        self.percent = kwargs.get("percent", self._percent)  # type: ignore
        self.strategy_type = kwargs.get("strategy_type", "random")  # type: ignore

    def target_definition(self) -> dict:
        model: dict = self.api_model()
        _target_definition: dict = {
            "strategyType": self.strategy_type,
            "strategy": dict(),
        }
        if model.get("percent", None):
            _target_definition["strategy"] = {"percentage": model["percent"]}
        elif model.get("exact", None):
            _target_definition["strategy"] = {"count": model["exact"]}
        else:
            error_msg: str = "Targeting was not properly defined"
            log.error(error_msg)
            raise GremlinCommandTargetError(error_msg)
        if type(model.get("containers")) == dict and model.get(
            "containers", dict()
        ).get("multiSelectLabels"):
            _target_definition["strategy"]["multiSelectLabels"] = model["containers"][
                "multiSelectLabels"
            ]
        if type(model.get("hosts")) == dict and model.get("hosts", dict()).get(
            "multiSelectLabels"
        ):
            _target_definition["strategy"]["multiSelectLabels"] = model["hosts"][
                "multiSelectLabels"
            ]
        return _target_definition

    def target_definition_graph(self) -> dict:
        model: dict = self.api_model()
        _target_definition: dict = {
            "strategy_type": self.strategy_type,
            "strategy": dict(),
        }
        if model.get("percent", None):
            _target_definition["strategy"] = {
                "type": "RandomPercent",
                "percentage": model["percent"],
            }
        elif model.get("exact", None):
            _target_definition["strategy"] = {"type": "Exact", "count": model["exact"]}
        else:
            error_msg: str = "Targeting was not properly defined"
            log.error(error_msg)
            raise GremlinCommandTargetError(error_msg)
        if type(model.get("containers")) == dict and model.get(
            "containers", dict()
        ).get("multiSelectLabels"):
            _target_definition["target_type"] = "Container"
            _target_definition["strategy"]["attrs"] = dict()
            _target_definition["strategy"]["attrs"]["multiSelectLabels"] = model[
                "containers"
            ]["multiSelectLabels"]
        if type(model.get("hosts")) == dict and model.get("hosts", dict()).get(
            "multiSelectLabels"
        ):
            _target_definition["target_type"] = "Host"
            _target_definition["strategy"]["attrs"] = dict()
            _target_definition["strategy"]["attrs"]["multiSelectLabels"] = model[
                "hosts"
            ]["multiSelectLabels"]
        return _target_definition

    @property
    def exact(self) -> int:
        return self._exact

    @exact.setter
    def exact(self, _exact: int = None) -> None:
        if not _exact:
            self._exact = 0
        elif isinstance(_exact, int) and _exact > 0:
            self._exact = _exact
            self._percent = 0
        else:
            error_msg: str = (
                f"Exact number of targets must be an integer greater than 0"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)

    @property
    def percent(self) -> int:
        return self._percent

    @percent.setter
    def percent(self, _percent: int = None) -> None:
        if not _percent:
            self._percent = 0
        elif isinstance(_percent, int) and 1 <= _percent <= 100:
            self._percent = _percent
            self._exact = 0
        else:
            error_msg: str = f"Target percentage must be an integer between 1 and 100"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)

    @property
    def strategy_type(self) -> str:
        return self._strategy_type

    @strategy_type.setter
    def strategy_type(self, _target_type: str = None) -> None:
        if not isinstance(_target_type, str) or not self._allowed_strategy_types.get(
            _target_type.lower(), None
        ):
            error_msg: str = f"strategy_type needs to be one of {str(self._allowed_strategy_types.keys())[1:-2]}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._strategy_type = self._allowed_strategy_types.get(
            _target_type.lower(), None
        )

    def api_model(self) -> dict:
        model: dict = dict()
        model["type"] = self.strategy_type
        if self.exact >= 0 and not self.percent:
            model["exact"] = str(self.exact)
        elif self.strategy_type == "Random":
            model["percent"] = self.percent
        else:
            error_msg: str = f"Type not correctly set, needs to be one of {str(self._allowed_strategy_types.keys())[1:-2]}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["exact"] = self.exact
        kwargs["percent"] = self.percent
        kwargs["strategy_type"] = self.strategy_type
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


class GremlinAttackCommandHelper(object):
    def __init__(self, *args: tuple, **kwargs: dict):
        self._length: int = 60
        self._commandType: str = ""
        self._shortType: str = ""
        self._typeMap: dict = {
            "cpu": "CPU",
            "memory": "Memory",
            "disk": "Disk",
            "io": "IO",
            "process_killer": "Process Killer",
            "shutdown": "Shutdown",
            "time_travel": "Time Travel",
            "blackhole": "Blackhole",
            "dns": "DNS",
            "latency": "Latency",
            "packet_loss": "Packet Loss",
        }
        self.length = kwargs.get("length", 60)  # type: ignore

    def impact_definition(self) -> dict:
        model: dict = self.api_model()
        _impact_definition: dict = {
            "commandArgs": {"cliArgs": [str(self.shortType)], "length": self.length},
            "commandType": str(self.shortType),
        }
        _impact_definition["commandArgs"]["cliArgs"].extend(model["args"])
        return _impact_definition

    def impact_definition_graph(self) -> dict:
        model: dict = self.api_model()
        _impact_definition: dict = {
            "infra_command_args": {
                "cli_args": [str(self.shortType)],
                "type": str(self.shortType),
            },
            "infra_command_type": str(self.shortType),
        }
        _impact_definition["infra_command_args"]["cli_args"].extend(model["args"])
        return _impact_definition

    @property
    def commandType(self) -> str:
        return self._commandType

    @commandType.setter
    def commandType(self, _commandType: str = None) -> None:
        if not isinstance(_commandType, str):
            error_msg: str = (
                f"commandType expects a string, received {type(_commandType)}"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        try:
            self._shortType = list(self._typeMap.keys())[
                list(self._typeMap.values()).index(_commandType)
            ]
        except ValueError:
            error_msg = (
                f"commandType needs to be one of: {str(self._typeMap.values())[1:-2]}"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._commandType = _commandType

    @property
    def length(self) -> int:
        return self._length

    @length.setter
    def length(self, _length: int = None) -> None:
        if not (
            isinstance(_length, int) and 1 <= _length <= 31449600
        ):  # Roughly 1 year in seconds
            error_msg: str = (
                f"Attack length needs to be an integer between 1 and 31449600"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._length = _length

    @property
    def shortType(self) -> str:
        return self._shortType

    @shortType.setter
    def shortType(self, _shortType: str = None) -> None:
        if not isinstance(_shortType, str):
            error_msg: str = f"type_ expects a string, received {type(_shortType)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        if not _shortType.lower() in self._typeMap:
            error_msg = f"invalid attack type, expected one of {str(self._typeMap.keys())[1:-2]}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._commandType = self._typeMap[_shortType]
        self._shortType = _shortType

    def api_model(self) -> dict:
        model: dict = {
            "type": self.shortType,
            "commandType": self.commandType,
            "args": ["-l", str(self.length)],
        }
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["length"] = self.length
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


class GremlinAttackHelper(object):
    def __init__(self, *args: tuple, **kwargs: dict):
        self._command: GremlinAttackCommandHelper = None  # type: ignore
        self._target: GremlinAttackTargetHelper = None  # type: ignore
        self.command: GremlinCPUAttack = kwargs.get("command", GremlinCPUAttack())  # type: ignore
        self.target: GremlinTargetHosts = kwargs.get("target", GremlinTargetHosts())  # type: ignore

    @property
    def command(self) -> GremlinAttackCommandHelper:
        return self._command

    @command.setter
    def command(self, _command: GremlinAttackCommandHelper) -> None:
        if not issubclass(type(_command), GremlinAttackCommandHelper):
            error_msg: str = f"Command needs to be a child class of {type(GremlinAttackCommandHelper)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        if issubclass(type(_command), GremlinTimeTravelAttack) and issubclass(
            type(self.target), GremlinTargetContainers
        ):
            error_msg = f"TimeTravel cannot target containers"
            log.error(error_msg)
            raise GremlinCommandTargetError(error_msg)
        self._command = _command

    @property
    def target(self) -> GremlinAttackTargetHelper:
        return self._target

    @target.setter
    def target(self, _target: GremlinAttackTargetHelper) -> None:
        if not issubclass(type(_target), GremlinAttackTargetHelper):
            error_msg: str = f"Command needs to be a child class of {type(GremlinAttackTargetHelper)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        if issubclass(type(_target), GremlinTargetContainers) and issubclass(
            type(self.command), GremlinTimeTravelAttack
        ):
            error_msg = f"TimeTravel cannot target containers"
            log.error(error_msg)
            raise GremlinCommandTargetError(error_msg)
        self._target = _target

    def api_model(self) -> dict:
        model: dict = {
            "target": self.target.api_model(),
            "command": self.command.api_model(),
        }
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["target"] = repr(self.target)
        kwargs["command"] = repr(self.command)
        return "%s(%s)" % (self.__class__.__name__, kwargs)

    def __str__(self) -> str:
        return repr(self)


class GremlinTargetHosts(GremlinAttackTargetHelper):
    def __init__(self, *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self._active_clients: list = list()
        self._active_identifiers: list = list()
        self._active_tags: dict = dict()
        self._ids: list = list()
        self._multiSelectTags: dict = dict()
        self._nativeTags: dict = {"os-type": "os_type", "os-version": "os_version"}
        self._target_all_hosts: bool = False
        self.target_all_hosts = kwargs.get("target_all_hosts", True)  # type: ignore

    # def target_definition(self):
    #     model = json.loads(self.__repr__())
    #     del model['type']
    #     _target_definition = super().target_definition()
    #     _target_definition['strategy'] = model
    #     _target_definition['targetType'] = 'Host'
    #     return _target_definition

    def target_definition(self) -> dict:
        _target_definition: dict = super().target_definition()
        _target_definition["targetType"] = "Host"
        return _target_definition

    @property
    def ids(self) -> list:
        return self._ids

    @ids.setter
    def ids(self, _ids: list = None) -> None:
        if not isinstance(_ids, list):
            error_msg: str = f"ids expects a list of strings, received {type(_ids)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        for _identifier in _ids:
            if not isinstance(_identifier, str):
                error_msg = (
                    f"Identifier not string; ids expect a string or list of strings"
                )
                log.error(error_msg)
                raise GremlinParameterError(error_msg)
            if self._valid_identifier(_identifier):
                self._ids.append(_identifier)
            else:
                error_msg = (
                    f'Target identifier "{_identifier}" not found in active clients'
                )
                log.warning(error_msg)
                raise GremlinIdentifierError(error_msg)
        self._multiSelectTags = {}
        self.target_all_hosts = False

    @property
    def tags(self) -> dict:
        return self._multiSelectTags

    @tags.setter
    def tags(self, _tags: dict = None) -> None:
        if isinstance(_tags, dict):
            for _tag in _tags:
                if self._valid_tag_pair(_tag, _tags[_tag]):
                    self._multiSelectTags[_tag] = _tags[_tag]
        self._ids = []
        self.target_all_hosts = False

    @property
    def target_all_hosts(self) -> bool:
        return self._target_all_hosts

    @target_all_hosts.setter
    def target_all_hosts(self, _target_all_hosts: bool = False) -> None:
        if _target_all_hosts != False:
            self._target_all_hosts = True
        else:
            self._target_all_hosts = False

    def _filter_active_identifiers(self) -> None:
        if not len(self._active_identifiers) > 0:
            self._load_active_clients()
            for _client in self._active_clients:
                self._active_identifiers.append(_client["identifier"])

    def _filter_active_tags(self) -> None:
        if not len(self._active_tags) > 0:
            self._load_active_clients()
            for _client in self._active_clients:
                for _tag in self._nativeTags:
                    if not self._active_tags.get(_tag):
                        self._active_tags[_tag] = list()
                    if _client.get(_tag) not in self._active_tags[_tag]:
                        self._active_tags[_tag].append(_client.get(_tag))
                for _tag in _client.get("tags"):
                    if not self._active_tags.get(_tag):
                        self._active_tags[_tag] = list()
                    _tag_value: str = _client["tags"].get(_tag)
                    if isinstance(_tag_value, str):
                        if _tag_value not in self._active_tags[_tag]:
                            self._active_tags[_tag].append(_tag_value)
                    elif isinstance(_tag_value, list):
                        for _inner_tag_value in _client["tags"].get(_tag):
                            if _inner_tag_value not in self._active_tags[_tag]:
                                self._active_tags[_tag].append(_inner_tag_value)

    def _load_active_clients(self) -> None:
        if not len(self._active_clients) > 0:
            self._active_clients = clients.list_active_clients()

    def _valid_identifier(self, identifier: str = None) -> bool:
        if not self._active_identifiers:
            self._filter_active_identifiers()
        if identifier in self._active_identifiers:
            return True
        return False

    def _valid_tag_pair(self, tagKey: str = None, tagValue: str = None) -> bool:
        if not self._active_tags:
            self._filter_active_tags()
        if tagValue in self._active_tags.get(tagKey, []):
            return True
        return False

    def api_model(self) -> dict:
        model: dict = super().api_model()
        if self.target_all_hosts:
            model["hosts"] = "all"
        else:
            if len(self.ids) > 0:
                model["hosts"] = {"ids": self.ids}
            elif len(self.tags) > 0:
                model["hosts"] = {"multiSelectTags": self.tags}
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["exact"] = self.exact
        kwargs["percent"] = self.percent
        kwargs["strategy_type"] = self.strategy_type
        kwargs["target_all_hosts"] = self.target_all_hosts
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


class GremlinTargetContainers(GremlinAttackTargetHelper):
    def __init__(self, *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self._active_containers: list = list()
        self._active_identifiers: list = list()
        self._active_labels: dict = dict()
        self._ids: list = list()
        self._multiSelectLabels: dict = dict()
        # self._nativeTags = {'os-type': 'os_type', 'os-version': 'os_version'}
        self._target_all_containers: bool = True
        self.target_all_containers = kwargs.get("target_all_containers", True)  # type: ignore
        self.ids = kwargs.get("ids", list())  # type: ignore
        self.labels = kwargs.get("labels", dict())

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

    def target_definition(self) -> dict:
        _target_definition: dict = super().target_definition()
        _target_definition["targetType"] = "Container"
        return _target_definition

    @property
    def ids(self) -> list:
        return self._ids

    @ids.setter
    def ids(self, _ids: list = None) -> None:
        if not isinstance(_ids, list):
            error_msg: str = f"ids expects a list of strings, received {type(_ids)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        if len(_ids) >= 1:
            for _identifier in _ids:
                if not isinstance(_identifier, str):
                    error_msg = (
                        f"Identifier not string; ids expect a string or list of strings"
                    )
                    log.error(error_msg)
                    raise GremlinParameterError(error_msg)
                if self._valid_identifier(_identifier):
                    self._ids.append(_identifier)
                else:
                    error_msg = (
                        f'Target identifier "{_identifier}" not found in active clients'
                    )
                    log.warning(error_msg)
                    raise GremlinIdentifierError(error_msg)
            self._multiSelectLabels = {}
            self.target_all_containers = False

    @property
    def labels(self) -> dict:
        return self._multiSelectLabels

    @labels.setter
    def labels(self, _labels: dict = None) -> None:
        if not isinstance(_labels, dict):
            error_msg: str = f"labels expects a dictionary, received {type(_labels)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        if bool(_labels):
            for _label in _labels:
                if isinstance(_labels[_label], str):
                    if self._valid_label_pair(_label, _labels[_label]):
                        if isinstance(self._multiSelectLabels.get(_label, None), list):
                            self._multiSelectLabels[_label].append(_labels[_label])
                        else:
                            self._multiSelectLabels[_label] = [_labels[_label]]
                elif isinstance(_labels[_label], list):
                    self._multiSelectLabels[_label] = list()
                    for _value in _labels[_label]:
                        if self._valid_label_pair(_label, _value):
                            self._multiSelectLabels[_label].append(_value)

            self._ids = []
            self.target_all_containers = False

    @property
    def target_all_containers(self) -> bool:
        return self._target_all_containers

    @target_all_containers.setter
    def target_all_containers(self, _target_all_containers: bool = False) -> None:
        if _target_all_containers != False:
            self._target_all_containers = True
        else:
            self._target_all_containers = False

    def _filter_active_identifiers(self) -> None:
        if not len(self._active_identifiers) > 0:
            self._load_active_containers()
            for _container in self._active_containers:
                self._active_identifiers.append(_container["identifier"])

    def _filter_active_labels(self) -> None:
        if not len(self._active_labels) > 0:
            self._load_active_containers()
            for _container in self._active_containers:
                for _label in _container.get("container_labels"):
                    if not self._active_labels.get(_label):
                        self._active_labels[_label] = list()
                    _label_value = _container["container_labels"].get(_label)
                    if isinstance(_label_value, str):
                        if _label_value not in self._active_labels[_label]:
                            self._active_labels[_label].append(_label_value)
                    elif isinstance(_label_value, list):
                        for _inner_label_value in _container["container_labels"].get(
                            _label
                        ):
                            if _inner_label_value not in self._active_labels[_label]:
                                self._active_labels[_label].append(_inner_label_value)

    def _load_active_containers(self) -> None:
        if not len(self._active_containers) > 0:
            self._active_containers = containers.list_containers()

    def _valid_identifier(self, identifier: str = None) -> bool:
        if not self._active_identifiers:
            self._filter_active_identifiers()
        if identifier in self._active_identifiers:
            return True
        return False

    def _valid_label_pair(self, labelKey: Any = None, labelValue: Any = None) -> bool:
        if not self._active_labels:
            self._filter_active_labels()
        if labelValue in self._active_labels.get(labelKey, []):
            return True
        return False

    def api_model(self) -> dict:
        model: dict = super().api_model()
        if self.target_all_containers:
            model["containers"] = "all"
        else:
            if len(self.ids) > 0:
                model["containers"] = {"ids": self.ids}
            elif len(self.labels) > 0:
                model["containers"] = {"multiSelectLabels": self.labels}
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["exact"] = self.exact
        kwargs["percent"] = self.percent
        kwargs["strategy_type"] = self.strategy_type
        kwargs["target_all_containers"] = self.target_all_containers
        kwargs["ids"] = self.ids
        kwargs["labels"] = self.labels
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


class GremlinResourceAttackHelper(GremlinAttackCommandHelper):
    def __init__(self, *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self._blocksize: int = 4
        self._directory: str = "/tmp"
        self._percent: int = 100
        self._workers: int = 1

    @property
    def blocksize(self) -> int:
        return self._blocksize

    @blocksize.setter
    def blocksize(self, _blocksize: int = None) -> None:
        if not (isinstance(_blocksize, int) and _blocksize >= 1):
            error_msg: str = f"blocksize requires a positive integer"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._blocksize = _blocksize

    @property
    def directory(self) -> str:
        return self._directory

    @directory.setter
    def directory(self, _directory: str = None) -> None:
        if not isinstance(_directory, str):
            error_msg: str = f"directory requires a string, received {type(_directory)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._directory = _directory

    @property
    def percent(self) -> int:
        return self._percent

    @percent.setter
    def percent(self, _percent: int = None) -> None:
        if not (isinstance(_percent, int) and 1 <= _percent <= 100):
            error_msg: str = f"percent is required to be an int between 1 and 100"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._percent = _percent

    @property
    def workers(self) -> int:
        return self._workers

    @workers.setter
    def workers(self, _workers: int = None) -> None:
        if not (isinstance(_workers, int) and _workers >= 1):
            error_msg: str = "workers requires a positive integer"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._workers = _workers

    def api_model(self) -> dict:
        model: dict = super().api_model()
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["length"] = self.length
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


class GremlinStateAttackHelper(GremlinAttackCommandHelper):
    def __init__(self, *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)

    def api_model(self) -> dict:
        model: dict = super().api_model()
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["length"] = self.length
        return "%s()" % (self.__class__.__name__)

    def __str__(self) -> str:
        return repr(self)


class GremlinNetworkAttackHelper(GremlinAttackCommandHelper):
    def __init__(self, *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self._allowed_protocols: list = ["ICMP", "TCP", "UDP"]
        self._ips: Union[str, list] = list()
        self._hostnames: Union[str, list] = ["^api.gremlin.com"]
        self._device: str = ""
        self._egress_ports: list = ["^53"]
        self._ids: list = []
        self._ingress_ports: list = list()
        self._multiSelectTags: dict = dict()
        self._port_regex: str = "([0-9]{1,4}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])"
        self._port_validator: Pattern = re.compile(
            f"^\^?{self._port_regex}(-{self._port_regex})?$"
        )
        self._protocol: str = ""
        self._providers: list = list()
        self._providers_filter: list = list()
        self._source_ports: list = list()
        self._tags: list = list()
        self._tags_filter = None
        self.device = kwargs.get("device", "")  # type: ignore
        self.ips = kwargs.get("ips", "")  # type: ignore
        self.protocol = kwargs.get("protocol", "")  # type: ignore
        self.providers = kwargs.get("providers", [])  # type: ignore
        self.tags = kwargs.get("tags", [])  # type: ignore

    def _filter_providers(self) -> None:
        _providers = providers.list_providers()
        for _provider in _providers:
            self._providers_filter.extend(
                getattr(providers, f"list_{_provider}_services")()
            )

    def _port_maker(self, _ports: list = None) -> list:
        port_list: list = list()
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
            error_msg: str = f"_port_maker expects a {type(str)} or {type(int)} or a {type(list)} of the previous types"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        return port_list

    def _valid_tag_pair(self, tagKey=None, tagValue=None) -> bool:
        return True

    def _validate_hostname(self, _hostname=None) -> bool:
        return True

    def _validate_ip(self, _ip: Union[str, list] = None) -> bool:
        return True

    def _validate_port_or_range(self, _port_or_range) -> bool:
        if not self._port_validator.match(_port_or_range):
            error_msg: str = f"{_port_or_range} is not a valid port or port range"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        return True

    def _validate_provider(self, _provider=None) -> bool:
        if not len(self._providers_filter) > 0:
            self._filter_providers()
        if _provider in self._providers_filter:
            return True
        return False

    @property
    def device(self) -> str:
        return self._device

    @device.setter
    def device(self, _device: str = None) -> None:
        if not _device:
            self._device = ""
            return
        elif not isinstance(_device, str):
            error_msg: str = f"device expects type {type(str)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._device = _device

    @property
    def egress_ports(self) -> list:
        return self._egress_ports

    @egress_ports.setter
    def egress_ports(self, _egress_ports: list = None) -> None:
        self._egress_ports = self._port_maker(_egress_ports)

    @property
    def ingress_ports(self) -> list:
        return self._ingress_ports

    @ingress_ports.setter
    def ingress_ports(self, _ingress_ports: list = None) -> None:
        self._ingress_ports = self._port_maker(_ingress_ports)

    @property
    def ips(self) -> Union[str, list]:
        return self._ips

    @ips.setter
    def ips(self, _ips: Union[str, list] = None) -> None:
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
            error_msg: str = f"valid ip addresses required"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)

    @property
    def hostnames(self) -> Union[str, list]:
        return self._hostnames

    @hostnames.setter
    def hostnames(self, _hostnames: Union[str, list] = None) -> None:
        if not _hostnames:
            pass
        elif isinstance(_hostnames, str):
            if not self._validate_hostname(_hostnames):
                error_msg: str = f"valid hostnames required"
                log.error(error_msg)
                raise GremlinParameterError(error_msg)
            self._hostnames = [_hostnames]
        elif isinstance(_hostnames, list):
            for _hostname in _hostnames:
                if not self._validate_hostname(_hostname):
                    error_msg = f"valid hostnames required"
                    log.error(error_msg)
                    raise GremlinParameterError(error_msg)
                self._hostnames = _hostname
        else:
            error_msg = f"hostnames requires a {type(str)} or {type(list)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)

    @property
    def protocol(self) -> str:
        return self._protocol

    @protocol.setter
    def protocol(self, _protocol=None) -> None:
        if not _protocol:
            self._protocol = ""
            return
        elif not (
            isinstance(_protocol, str) and _protocol.upper() in self._allowed_protocols
        ):
            error_msg: str = f"Protocol must be a string and one of {str(self._allowed_protocols)[1:-2]}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._protocol = _protocol.upper()

    @property
    def providers(self) -> list:
        return self._providers

    @providers.setter
    def providers(self, _providers: Union[str, list] = None) -> None:
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
            error_msg: str = f"providers expect a {type(str)} or {type(list)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)

    @property
    def source_ports(self) -> list:
        return self._source_ports

    @source_ports.setter
    def source_ports(self, _source_ports: list = None) -> None:
        self._source_ports = self._port_maker(_source_ports)

    @property
    def tags(self) -> list:
        return self._tags

    @tags.setter
    def tags(self, _tags: Union[list, dict] = None) -> None:
        if isinstance(_tags, dict):
            for _tag in _tags:
                if self._valid_tag_pair(_tag, _tags[_tag]):
                    self._multiSelectTags[_tag] = _tags[_tag]
        self._ids = []
        self.target_all_hosts = False

    def api_model(self) -> dict:
        model: dict = super().api_model()
        if self.device:
            model["args"].extend(["-d", self.device])
        if len(self.ips) > 0:
            model["args"].extend(["-i", ",".join(self.ips)])
        if self.protocol:
            model["args"].extend(["-P", self.protocol])
        if self.providers and len(self.providers) > 0:
            model["providers"] = self.providers
        if self.tags and len(self.tags) > 0:
            model["trafficImpactMapping"] = {"multiSelectTags": self.tags}
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["length"] = self.length
        kwargs["device"] = self.device
        kwargs["ips"] = self.ips
        kwargs["protocol"] = self.protocol
        kwargs["providers"] = self.providers
        kwargs["tags"] = self.tags
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


class GremlinCPUAttack(GremlinResourceAttackHelper):
    def __init__(self, *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.shortType: str = "cpu"
        self._all_cores: bool = False  # ['-a']
        self._capacity: int = 100  # ['-p', int]
        self._cores: int = 1  # ['-c', int]
        self.all_cores = kwargs.get("all_cores", False)  # type: ignore
        self.capacity = kwargs.get("capacity", 100)  # type: ignore
        self.cores = kwargs.get("cores", 1)  # type: ignore

    @property
    def all_cores(self) -> bool:
        return self._all_cores

    @all_cores.setter
    def all_cores(self, _all_cores: bool = None) -> None:
        if not isinstance(_all_cores, bool):
            error_msg: str = f"all_cores expects a bool, received {type(_all_cores)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._all_cores = _all_cores

    @property
    def capacity(self) -> int:
        return self._capacity

    @capacity.setter
    def capacity(self, _capacity: int = None) -> None:
        if not (isinstance(_capacity, int) and 1 <= _capacity <= 100):
            error_msg: str = f"Capacity expects an integer between 1 and 100"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._capacity = _capacity

    @property
    def cores(self) -> int:
        return self._cores

    @cores.setter
    def cores(self, _cores: int = None) -> None:
        if not (isinstance(_cores, int) and _cores >= 1):
            error_msg: str = f"Cores expects a positive integer"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._cores = _cores

    def api_model(self) -> dict:
        model: dict = super().api_model()
        model["args"].extend(["-p", str(self.capacity)])
        if self.all_cores:
            model["args"].append("-a")
        else:
            model["args"].extend(["-c", str(self.cores)])
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["all_cores"] = self.all_cores
        kwargs["capacity"] = self.capacity
        kwargs["cores"] = self.cores
        kwargs["length"] = self.length
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


class GremlinMemoryAttack(GremlinResourceAttackHelper):
    def __init__(self, *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.shortType: str = "memory"
        self._allowedAmountTypes: list = ["MB", "GB", "%"]
        self._amount: int = 75
        self._amountType: str = "%"
        self.amount = kwargs.get("amount", 100)  # type: ignore
        self.amountType = kwargs.get("amountType", "%")  # type: ignore

    # def impact_definition(self):
    #     model = json.loads(self.__repr__())
    #     _impact_definition = super().impact_definition()
    #     _impact_definition['commandArgs']['cliArgs'].extend(model['args'])
    #     return _impact_definition

    @property
    def amount(self) -> int:
        return self._amount

    @amount.setter
    def amount(self, _amount: int = None) -> None:
        if not (isinstance(_amount, int) and _amount >= 1):
            error_msg: str = (
                f"amount expects a positive integer, received {type(_amount)}"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        if self.amountType == "%" and not 1 <= _amount <= 100:
            error_msg = f"amount must be an integer between 1 and 100 when amountType is set to %"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._amount = _amount

    @property
    def amountType(self) -> str:
        return self._amountType

    @amountType.setter
    def amountType(self, _amountType: str = None) -> None:
        if not (
            isinstance(_amountType, str)
            and _amountType.upper() in self._allowedAmountTypes
        ):
            error_msg: str = f"amountType expects a string with a value belonging to {str(self._allowedAmountTypes)[1:-2]}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        if _amountType == "%" and not 1 <= self.amount <= 100:
            error_msg = (
                f"amountType cannot be set to % while amount is not between 1 and 100"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._amountType = _amountType.upper()

    def api_model(self) -> dict:
        model: dict = super().api_model()
        if self.amountType == "MB":
            model["args"].extend(["-m", str(self.amount)])
        elif self.amountType == "GB":
            model["args"].extend(["-g", str(self.amount)])
        elif self.amountType == "%":
            model["args"].extend(["-p", str(self.amount)])
        else:
            error_msg: str = f"Fatal error, data model may be corrupted, amountType: {self._amountType} is not valid"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["length"] = self.length
        kwargs["amount"] = self.amount
        kwargs["amountType"] = self.amountType
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


class GremlinDiskSpaceAttack(GremlinResourceAttackHelper):
    def __init__(self, *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.shortType: str = "disk"
        self.blocksize: int = kwargs.get("blocksize", 4)  # type: ignore
        self.directory: str = kwargs.get("directory", "/tmp")  # type: ignore
        self.percent: int = kwargs.get("percent", 100)  # type: ignore
        self.workers: int = kwargs.get("workers", 1)  # type: ignore

    def api_model(self) -> dict:
        model: dict = super().api_model()
        model["args"].extend(["-d", str(self.directory)])
        model["args"].extend(["-w", str(self.workers)])
        model["args"].extend(["-b", str(self.blocksize)])
        model["args"].extend(["-p", str(self.percent)])
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["length"] = self.length
        kwargs["blocksize"] = self.blocksize
        kwargs["directory"] = self.directory
        kwargs["percent"] = self.percent
        kwargs["workers"] = self.workers
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


class GremlinDiskIOAttack(GremlinResourceAttackHelper):
    def __init__(self, *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.shortType: str = "io"
        self._allowed_modes: list = ["r", "rw", "w"]
        self._blockcount: int = 1
        self._mode: str = "rw"
        self.blockcount: int = kwargs.get("blockcount", 1)  # type: ignore
        self.blocksize: int = kwargs.get("blocksize", 4)  # type: ignore
        self.directory: str = kwargs.get("directory", "/tmp")  # type: ignore
        self.mode: str = kwargs.get("mode", "rw")  # type: ignore
        self.workers: int = kwargs.get("workers", 1)  # type: ignore

    @property
    def blockcount(self) -> int:
        return self._blockcount

    @blockcount.setter
    def blockcount(self, _blockcount: int = None) -> None:
        if not (isinstance(_blockcount, int) and _blockcount >= 1):
            error_msg: str = f"blockcount requires a positive integer"
            if log.getEffectiveLevel() == logging.DEBUG:
                log.debug(error_msg)
            raise GremlinParameterError(error_msg)
        self._blockcount = _blockcount

    @property
    def mode(self) -> str:
        return self._mode

    @mode.setter
    def mode(self, _mode: str = None) -> None:
        if not (isinstance(_mode, str) and _mode.lower() in self._allowed_modes):
            error_msg: str = f"mode needs to be one of {str(self._allowed_modes)[1:-2]}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._mode = _mode.lower()

    def api_model(self) -> dict:
        model: dict = super().api_model()
        model["args"].extend(["-c", str(self.blockcount)])
        model["args"].extend(["-d", self.directory])
        model["args"].extend(["-m", self.mode])
        model["args"].extend(["-s", str(self.blocksize)])
        model["args"].extend(["-w", str(self.workers)])
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["length"] = self.length
        kwargs["blockcount"] = self.blockcount
        kwargs["blocksize"] = self.blocksize
        kwargs["directory"] = self.directory
        kwargs["mode"] = self.mode
        kwargs["workers"] = self.workers
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


class GremlinShutdownAttack(GremlinStateAttackHelper):
    def __init__(self, *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.shortType: str = "shutdown"
        self._delay: int = 1
        self._reboot: bool = False
        self.delay: int = kwargs.get("delay", 1)  # type: ignore
        self.reboot: bool = kwargs.get("reboot", False)  # type: ignore

    @property
    def delay(self) -> int:
        return self._delay

    @delay.setter
    def delay(self, _delay: int = None) -> None:
        if not (isinstance(_delay, int) and _delay >= 1):
            error_msg: str = f"delay expects a positive {type(int)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._delay = _delay

    @property
    def reboot(self) -> bool:
        return self._reboot

    @reboot.setter
    def reboot(self, _reboot: bool = None) -> None:
        if not isinstance(_reboot, bool):
            error_msg: str = f"reboot expects a {type(bool)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._reboot = _reboot

    def api_model(self) -> dict:
        model: dict = super().api_model()
        model["args"] = ["-d", str(self.delay)]
        if self.reboot:
            model["args"].append("-r")
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["length"] = self.length
        kwargs["delay"] = self.delay
        kwargs["reboot"] = self.reboot
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


class GremlinProcessKillerAttack(GremlinStateAttackHelper):
    def __init__(self, *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.shortType: str = "process_killer"
        self._exact: bool = False
        self._full_match: bool = False
        self._group: str = str()
        self._interval: int = 1
        self._kill_children: bool = False
        self._process: str = str()
        self._target_newest: bool = False
        self._target_oldest: bool = False
        self._user: str = str()
        self.exact: bool = kwargs.get("exact", False)  # type: ignore
        self.full_match: bool = kwargs.get("full_match", False)  # type: ignore
        self.group: str = kwargs.get("group", str())  # type: ignore
        self.interval: int = kwargs.get("interval", 1)  # type: ignore
        self.kill_children: bool = kwargs.get("kill_children", False)  # type: ignore
        self.process: str = kwargs.get("process", str())  # type: ignore
        self.target_newest: bool = kwargs.get("target_newest", False)  # type: ignore
        self.target_oldest: bool = kwargs.get("target_oldest", False)  # type: ignore
        self.user: str = kwargs.get("user", str())  # type: ignore

    @property
    def exact(self) -> bool:
        return self._exact

    @exact.setter
    def exact(self, _exact: bool = None) -> None:
        if not isinstance(_exact, bool):
            error_msg: str = f"exact expects type {type(bool)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._exact = _exact

    @property
    def full_match(self) -> bool:
        return self._full_match

    @full_match.setter
    def full_match(self, _full_match: bool = None) -> None:
        if not _full_match:
            self._full_match = False
        elif not isinstance(_full_match, bool):
            error_msg: str = f"exact expects type {type(bool)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._full_match = True

    @property
    def group(self) -> str:
        return self._group

    @group.setter
    def group(self, _group: str = None) -> None:
        if not isinstance(_group, str):
            error_msg: str = f"group expects type {type(str)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._group = _group

    @property
    def interval(self) -> int:
        return self._interval

    @interval.setter
    def interval(self, _interval: int = None) -> None:
        if not (isinstance(_interval, int) and _interval >= 1):
            error_msg: str = f"group expects positive integer of type {type(int)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._interval = _interval

    @property
    def kill_children(self) -> bool:
        return self._kill_children

    @kill_children.setter
    def kill_children(self, _kill_children: bool = None) -> None:
        if not isinstance(_kill_children, bool):
            error_msg: str = f"kill_children expects {type(bool)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._kill_children = _kill_children

    @property
    def process(self) -> str:
        return self._process

    @process.setter
    def process(self, _process: str = None) -> None:
        if not isinstance(_process, str):
            error_msg: str = f"process expects {type(str)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._process = _process

    @property
    def target_newest(self) -> bool:
        return self._target_newest

    @target_newest.setter
    def target_newest(self, _target_newest: bool = None) -> None:
        if isinstance(_target_newest, bool):
            if _target_newest == True:
                self._target_newest = True
                self._target_oldest = False
            else:
                self._target_newest = False
        else:
            error_msg: str = f"target_newest expects type {type(bool)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)

    @property
    def target_oldest(self) -> bool:
        return self._target_oldest

    @target_oldest.setter
    def target_oldest(self, _target_oldest: bool = None) -> None:
        if isinstance(_target_oldest, bool):
            if _target_oldest == True:
                self._target_oldest = True
                self._target_newest = False
            else:
                self._target_oldest = False
        else:
            error_msg: str = f"target_oldest expects type {type(bool)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)

    @property
    def user(self) -> str:
        return self._user

    @user.setter
    def user(self, _user: str = None) -> None:
        if not _user:
            self._user = ""
        elif isinstance(_user, str):
            self._user = _user
        else:
            error_msg: str = f"user expects {type(str)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)

    def api_model(self) -> dict:
        model: dict = super().api_model()
        model["args"].extend(["-i", str(self.interval)])
        if self.group:
            model["args"].extend(["-g", self.group])
        if self.process:
            model["args"].extend(["-p", self.process])
        else:
            error_msg: str = f"process is required to a be a non-empty string"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        if self.user:
            model["args"].extend(["-u", self.user])
        if self.exact:
            model["args"].append("-e")
        if self.full_match:
            model["args"].append("-f")
        if self.kill_children:
            model["args"].append("-c")
        if self.target_newest and not self.target_oldest:
            model["args"].append("-n")
        if self.target_oldest and not self.target_newest:
            model["args"].append("-o")
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["length"] = self.length
        kwargs["exact"] = self.exact
        kwargs["full_match"] = self.full_match
        kwargs["group"] = self.group
        kwargs["interval"] = self.interval
        kwargs["kill_children"] = self.kill_children
        kwargs["process"] = self.process
        kwargs["target_newest"] = self.target_newest
        kwargs["target_oldest"] = self.target_oldest
        kwargs["user"] = self.user
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


class GremlinTimeTravelAttack(GremlinStateAttackHelper):
    def __init__(self, *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.shortType: str = "time_travel"
        self._block_ntp: bool = False
        self._offset: int = 86400
        self.block_ntp: bool = kwargs.get("block_ntp", False)  # type: ignore
        self.offset: int = kwargs.get("offset", 86400)  # type: ignore

    @property
    def block_ntp(self) -> bool:
        return self._block_ntp

    @block_ntp.setter
    def block_ntp(self, _block_ntp: bool = None) -> None:
        if not isinstance(_block_ntp, bool):
            error_msg: str = f"block_ntp expects type {type(bool)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._block_ntp = _block_ntp

    @property
    def offset(self) -> int:
        return self._offset

    @offset.setter
    def offset(self, offset: int = None) -> None:
        if not isinstance(offset, int):
            error_msg: str = f"Offset needs to be an integer, received {type(offset)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._offset = offset

    def api_model(self) -> dict:
        model: dict = super().api_model()
        model["args"].extend(["-o", str(self.offset)])
        if self.block_ntp:
            model["args"].append("-n")
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["length"] = self.length
        kwargs["block_ntp"] = self.block_ntp
        kwargs["offset"] = self.offset
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


class GremlinBlackholeAttack(GremlinNetworkAttackHelper):
    def __init__(self, *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.shortType: str = "blackhole"
        self.egress_ports: list = kwargs.get("egress_ports", ["^53"])  # type: ignore
        self.hostnames: str = kwargs.get("hostnames", "^api.gremlin.com")  # type: ignore
        self.ingress_ports: list = kwargs.get("ingress_ports", [])  # type: ignore

    def api_model(self) -> dict:
        model: dict = super().api_model()
        if len(self.egress_ports) > 0:
            model["args"].extend(["-p", ",".join(self.egress_ports)])
        if len(self.hostnames) > 0:
            model["args"].extend(["-h", ",".join(self.hostnames)])
        if len(self.ingress_ports) > 0:
            model["args"].extend(["-n", ",".join(self.ingress_ports)])
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["length"] = self.length
        kwargs["device"] = self.device
        kwargs["ips"] = self.ips
        kwargs["protocol"] = self.protocol
        kwargs["providers"] = self.providers
        kwargs["tags"] = self.tags
        kwargs["egress_ports"] = self.egress_ports
        kwargs["hostnames"] = self.hostnames
        kwargs["ingress_ports"] = self.ingress_ports
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


class GremlinDNSAttack(GremlinNetworkAttackHelper):
    def __init__(self, *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.shortType: str = "dns"
        self._allowed_protocols: list = ["TCP", "UDP"]
        self.protocol: str = kwargs.get("protocol", "")  # type: ignore

    def api_model(self) -> dict:
        model: dict = super().api_model()
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["length"] = self.length
        kwargs["device"] = self.device
        kwargs["ips"] = self.ips
        kwargs["protocol"] = self.protocol
        kwargs["providers"] = self.providers
        kwargs["tags"] = self.tags
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


class GremlinLatencyAttack(GremlinNetworkAttackHelper):
    def __init__(self, *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.shortType: str = "latency"
        self._delay: int = 100
        self.delay: int = kwargs.get("delay", 100)  # type: ignore
        self.egress_ports: list = kwargs.get("egress_ports", ["^53"])  # type: ignore
        self.hostnames: str = kwargs.get("hostnames", "^api.gremlin.com")  # type: ignore
        self.source_ports: list = kwargs.get("source_ports", [])  # type: ignore

    @property
    def delay(self) -> int:
        return self._delay

    @delay.setter
    def delay(self, _delay: int = None) -> None:
        if not (isinstance(_delay, int) and _delay >= 1):
            error_msg: str = f"delay expects a positive integer type {type(int)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._delay = _delay

    def api_model(self) -> dict:
        model: dict = super().api_model()
        model["args"].extend(["-m", str(self.delay)])
        if len(self.egress_ports) > 0:
            model["args"].extend(["-p", ",".join(self.egress_ports)])
        if len(self.hostnames) > 0:
            model["args"].extend(["-h", ",".join(self.hostnames)])
        if len(self.source_ports) > 0:
            model["args"].extend(["-s", ",".join(self.source_ports)])
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["length"] = self.length
        kwargs["device"] = self.device
        kwargs["ips"] = self.ips
        kwargs["protocol"] = self.protocol
        kwargs["providers"] = self.providers
        kwargs["tags"] = self.tags
        kwargs["delay"] = self.delay
        kwargs["egress_ports"] = self.egress_ports
        kwargs["hostnames"] = self.hostnames
        kwargs["source_ports"] = self.source_ports
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


class GremlinPacketLossAttack(GremlinNetworkAttackHelper):
    def __init__(self, *args: tuple, **kwargs: dict):
        super().__init__(*args, **kwargs)
        self.shortType: str = "packet_loss"
        self._corrupt: bool = False
        self._percent: int = 1
        self.corrupt: bool = kwargs.get("corrupt", False)  # type: ignore
        self.egress_ports: list = kwargs.get("egress_ports", ["^53"])  # type: ignore
        self.hostnames: str = kwargs.get("hostnames", "^api.gremlin.com")  # type: ignore
        self.percent: int = kwargs.get("percent", 1)  # type: ignore
        self.source_ports: list = kwargs.get("source_ports", [])  # type: ignore

    @property
    def corrupt(self) -> bool:
        return self._corrupt

    @corrupt.setter
    def corrupt(self, _corrupt: bool = None) -> None:
        if not _corrupt:
            self._corrupt = False
            return
        if not isinstance(_corrupt, bool):
            error_msg: str = f"corrupt expects type {type(bool)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._corrupt = _corrupt

    @property
    def percent(self) -> int:
        return self._percent

    @percent.setter
    def percent(self, _percent: int = None) -> None:
        if not (isinstance(_percent, int) and 1 <= _percent <= 100):
            error_msg: str = (
                f"percent expects positive integer type {type(int)} between 1 and 100"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._percent = _percent

    def api_model(self) -> dict:
        model: dict = super().api_model()
        model["args"].extend(["-r", str(self.percent)])
        if len(self.egress_ports) > 0:
            model["args"].extend(["-p", ",".join(self.egress_ports)])
        if len(self.hostnames) > 0:
            model["args"].extend(["-h", ",".join(self.hostnames)])
        if len(self.source_ports) > 0:
            model["args"].extend(["-s", ",".join(self.source_ports)])
        if self.corrupt:
            model["args"].append("-c")
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["length"] = self.length
        kwargs["device"] = self.device
        kwargs["ips"] = self.ips
        kwargs["protocol"] = self.protocol
        kwargs["providers"] = self.providers
        kwargs["tags"] = self.tags
        kwargs["corrupt"] = self.corrupt
        kwargs["egress_ports"] = self.egress_ports
        kwargs["hostnames"] = self.hostnames
        kwargs["percent"] = self.percent
        kwargs["source_ports"] = self.source_ports
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)
