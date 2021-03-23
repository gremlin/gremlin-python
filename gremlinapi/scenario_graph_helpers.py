# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import inspect
import json
import logging
import uuid
from typing import Union, Optional

from gremlinapi.exceptions import (
    GremlinCommandTargetError,
    GremlinIdentifierError,
    GremlinParameterError,
)

from gremlinapi.attack_helpers import (
    GremlinAttackCommandHelper,
    GremlinAttackTargetHelper,
)
from gremlinapi.clients import GremlinAPIClients as clients
from gremlinapi.containers import GremlinAPIContainers as containers
from gremlinapi.providers import GremlinAPIProviders as providers

# from gremlinapi.scenario_graph_helpers import GremlinScenarioNode

log = logging.getLogger("GremlinAPI.client")


class GremlinScenarioNode(object):
    def __init__(
        self,
        *args: tuple,
        **kwargs: dict,
    ):
        self._edges: dict = dict()
        self._id: str = str()
        self._previous: "GremlinScenarioNode" = None  # type: ignore
        self._name: str = str()
        self._next: "GremlinScenarioNode" = None  # type: ignore
        self._node_type: str = str()
        self.id: str = str(uuid.uuid4())
        self.name: str = kwargs.get("name", None)  # type: ignore

    def add_edge(self, _node: "GremlinScenarioNode", _weight: str = None) -> None:
        if not issubclass(type(_node), GremlinScenarioNode):
            error_msg: str = (
                f"add_edge expects a GremlinScenarioNode, received {type(_node)}"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._edges[_node.id] = {"node": _node, "weight": _weight}

    @property
    def data(self) -> dict:
        return self.repr_model()

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, _id: str = None) -> None:
        if not isinstance(_id, str):
            error_msg: str = f"id expects a string {type(str)}, received {type(str)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._id = _id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, _name: str = None) -> None:
        if not isinstance(_name, str):
            error_msg: str = (
                f"name expects type string {type(str)}, received {type(_name)}"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._name = _name

    @property
    def next(self) -> "GremlinScenarioNode":
        return self._next

    @next.setter
    def next(self, _node: "GremlinScenarioNode") -> None:
        if not issubclass(type(_node), GremlinScenarioNode):
            error_msg: str = (
                f"next expects a GremlinScenarioNode, received {type(_node)}"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._next = _node

    @property
    def node_type(self) -> str:
        return self._node_type

    @node_type.setter
    def node_type(self, _node_type: str = None) -> None:
        if not isinstance(_node_type, str):
            error_msg: str = (
                f"node_type expects string {type(str)}, received {type(_node_type)}"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._node_type = _node_type

    @property
    def previous(self) -> "GremlinScenarioNode":
        return self._previous

    @previous.setter
    def previous(self, _node: "GremlinScenarioNode") -> None:
        if not issubclass(type(_node), GremlinScenarioNode):
            error_msg: str = (
                f"previous expects a GremlinScenarioNode, received {type(_node)}"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._previous = _node

    @property
    def uuid(self) -> str:
        if not self.name:
            error_msg: str = f"Node Name is required to build a scenario node, please set a node name"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        return f"{self.name}-{self.id}"

    def repr_model(self) -> dict:
        if not self.next:
            model = {"type": self.node_type, "id": self.uuid, "next": None}
        else:
            model = {"type": self.node_type, "id": self.uuid, "next": self.next.uuid}
        return model

    def __repr__(self) -> str:
        return json.dumps(self.repr_model)


class GremlinScenarioGraphHelper(object):
    def __init__(
        self,
        *args: tuple,
        **kwargs: dict,
    ):
        self._description: str = str()
        self._hypothesis: str = str()
        self._name: str = str()
        self._nodes: _GremlinNodeGraph = _GremlinNodeGraph()
        self._start = str()
        self.description: str = kwargs.get("description", None)  # type: ignore
        self.hypothesis: str = kwargs.get("hypothesis", None)  # type: ignore
        self.name: str = kwargs.get("name", None)  # type: ignore

    def add_node(self, _node: GremlinScenarioNode) -> None:
        if not issubclass(type(_node), GremlinScenarioNode):
            error_msg: str = f"add_node expects GremlinScenarioNode (or None), received {type(_node)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._nodes.append(_node)

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, _description: str = None) -> None:
        if not isinstance(_description, str):
            error_msg: str = f"Description expects string {type(str())}, received {type(_description)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._description = _description

    @property
    def hypothesis(self) -> str:
        return self._hypothesis

    @hypothesis.setter
    def hypothesis(self, _hypothesis: str = None) -> None:
        if not isinstance(_hypothesis, str):
            error_msg: str = (
                f"Hypothesis expects string {type(str())}, received {type(_hypothesis)}"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._hypothesis = _hypothesis

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, _name: str = None) -> None:
        if not isinstance(_name, str):
            error_msg: str = (
                f"Name expects string {type(str())}, received {type(_name)}"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._name = _name

    def repr_model(self) -> dict:
        model: dict = {
            "description": self.description,
            "hypothesis": self.hypothesis,
            "name": self.name,
        }
        if self._nodes.head is not None:
            model["graph"] = {
                "start_id": self._nodes.head.uuid,
                "nodes": {
                    node.uuid: data for node, data in self._nodes.nodes_data_linear()
                },
            }
        return model

    def __repr__(self) -> str:
        model: dict = self.repr_model()
        return json.dumps(model)


class GremlinScenarioAttackNode(GremlinScenarioNode):
    def __init__(
        self,
        *args: tuple,
        **kwargs: dict,
    ):
        super().__init__(*args, **kwargs)
        self.node_type: str = "attack"
        self._attack_type: str = str()

    @property
    def attack_type(self) -> str:
        return self._attack_type

    @attack_type.setter
    def attack_type(self, _attack_type: str = None) -> None:
        if not isinstance(_attack_type, str):
            error_msg: str = (
                f"attack_type expects string {type(str)}, received {type(_attack_type)}"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._attack_type = _attack_type


class GremlinScenarioILFINode(GremlinScenarioAttackNode):
    def __init__(self, *args: tuple, **kwargs: dict):
        if not kwargs.get("name", None) and kwargs.get("command", None):  # type: ignore
            kwargs["name"] = (kwargs.get("command")).shortType  # type: ignore
        super().__init__(*args, **kwargs)
        self._command: GremlinAttackCommandHelper = None  # type: ignore
        self._target: GremlinAttackTargetHelper = None  # type: ignore
        self.node_type: str = "InfraAttack"
        self.command: GremlinAttackCommandHelper = kwargs.get("command", self._command)  # type: ignore
        self.target: GremlinAttackTargetHelper = kwargs.get("target", self._target)  # type: ignore

    @property
    def command(self) -> GremlinAttackCommandHelper:
        return self._command

    @command.setter
    def command(self, _command: GremlinAttackCommandHelper) -> None:
        if not issubclass(type(_command), GremlinAttackCommandHelper):
            error_msg: str = f"impact_definition expects a GremlinAttackCommandHelper, received {type(_command)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._command = _command

    def repr_model(self) -> dict:
        model: dict = super().repr_model()
        model["impact_definition"] = self.command.impact_definition_graph()
        model["target_definition"] = self.target.target_definition_graph()
        return model

    @property
    def target(self) -> GremlinAttackTargetHelper:
        return self._target

    @target.setter
    def target(self, _target: GremlinAttackTargetHelper) -> None:
        if not issubclass(type(_target), GremlinAttackTargetHelper):
            error_msg: str = f"target_definition expects a GremlinAttackTargetHelper, received {type(_target)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._target = _target


class GremlinScenarioALFINode(GremlinScenarioAttackNode):
    def __init__(
        self,
        *args: tuple,
        **kwargs: dict,
    ):
        super().__init__(*args, **kwargs)
        self.attack_type = "ALFI"
        raise NotImplementedError("ALFI Scenarios NOT IMPLEMENTED")


class GremlinScenarioDelayNode(GremlinScenarioNode):
    def __init__(self, *args: tuple, **kwargs: dict):
        if not kwargs.get("name", None):
            kwargs["name"] = "Delay"  # type: ignore
        super().__init__(*args, **kwargs)
        self._delay: int = int()
        self._delay: int = kwargs.get("delay", None)  # type: ignore
        self.node_type: str = "Delay"

    def repr_model(self) -> dict:
        model: dict = super().repr_model()
        model["delay"] = self.delay
        return model

    @property
    def delay(self) -> int:
        return self._delay

    @delay.setter
    def delay(self, _duration: int = None) -> None:
        if not isinstance(_duration, int):
            error_msg: str = (
                f"delay expects int type {type(int)}, received {type(_duration)}"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._delay = _duration


class GremlinScenarioStatusCheckNode(GremlinScenarioNode):
    def __init__(
        self,
        *args: tuple,
        **kwargs: dict,
    ):
        if not kwargs.get("name", None):
            kwargs["name"] = "status-check"  # type: ignore
        super().__init__(*args, **kwargs)
        self.node_type: str = "SynchronousStatusCheck"
        self._description: str = str()
        self._endpoint_url: str = str()
        self._endpoint_headers: dict = {}
        self._evaluation_ok_status_codes: list = list()
        self._evaluation_ok_latency_max: int = int()
        self._evaluation_response_body_evaluation: str = ""
        self.description: str = kwargs.get("description", None)  # type: ignore
        self.endpoint_url: str = kwargs.get("endpoint_url", None)  # type: ignore
        self.endpoint_headers: dict = kwargs.get("endpoint_headers", None)  # type: ignore
        self.evaluation_ok_status_codes: list = kwargs.get(
            "evaluation_ok_status_codes", ["200-203"]
        )  # type: ignore
        self.evaluation_ok_latency_max: int = kwargs.get("evaluation_ok_latency_max", 500)  # type: ignore
        self.evaluation_response_body_evaluation: str = kwargs.get(
            "evaluation_response_body_evaluation", ""
        )  # type: ignore

    def repr_model(self) -> dict:
        model: dict = super().repr_model()
        model["endpointConfiguration"] = {
            "url": self.endpoint_url,
            "headers": self.endpoint_headers,
        }
        model["evaluationConfiguration"] = {
            "okStatusCodes": self.evaluation_ok_status_codes,
            "okLatencyMaxMs": self.evaluation_ok_latency_max,
            "responseBodyEvaluation": self.evaluation_response_body_evaluation,
        }
        model["thirdPartyPresets"] = "PythonSDK"
        return model

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, _description: str = None) -> None:
        if not isinstance(_description, str):
            error_msg: str = (
                f"description expects string, received {type(_description)}"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._description = _description

    @property
    def endpoint_headers(self) -> dict:
        return self._endpoint_headers

    @endpoint_headers.setter
    def endpoint_headers(self, _headers: dict = {}) -> None:
        self._endpoint_headers = _headers

    @property
    def endpoint_url(self) -> str:
        return self._endpoint_url

    @endpoint_url.setter
    def endpoint_url(self, _url: str = None) -> None:
        if not isinstance(_url, str):
            error_msg: str = f"url expects a valid url string, received {type(_url)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._endpoint_url = _url

    @property
    def evaluation_ok_status_codes(self) -> list:
        return self._evaluation_ok_status_codes

    @evaluation_ok_status_codes.setter
    def evaluation_ok_status_codes(self, _status_codes: list = None) -> None:
        if not isinstance(_status_codes, list):
            error_msg: str = f"evaluation_ok_status_codes expects a list of integers or strings, received {type(_status_codes)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._evaluation_ok_status_codes = _status_codes

    @property
    def evaluation_ok_latency_max(self) -> int:
        return self._evaluation_ok_latency_max

    @evaluation_ok_latency_max.setter
    def evaluation_ok_latency_max(self, _latency: int = None) -> None:
        if not isinstance(_latency, int):
            error_msg: str = (
                f"evaluation_ok_latency_max expects an int, received {type(_latency)}"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._evaluation_ok_latency_max = _latency

    @property
    def evaluation_response_body_evaluation(self) -> str:
        return self._evaluation_response_body_evaluation

    @evaluation_response_body_evaluation.setter
    def evaluation_response_body_evaluation(
        self, _evaluation_response_body_evaluation: str = None
    ) -> None:
        if not _evaluation_response_body_evaluation:
            error_msg: str = f"evaluation_response_body_evaluation expects an argument, none provided"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._evaluation_response_body_evaluation = _evaluation_response_body_evaluation


class _GremlinNodeGraph(object):
    def __init__(self):
        self._head: GremlinScenarioNode = None  # type: ignore

    def add_edge(
        self,
        src_node: GremlinScenarioNode,
        dest_node: GremlinScenarioNode,
        _weight=None,
    ) -> None:
        self._validate_type(src_node)
        self._validate_type(dest_node)
        src_node.add_edge(dest_node, _weight)
        dest_node.add_edge(src_node, _weight)

    def append(self, new_node: GremlinScenarioNode) -> None:
        self._validate_type(new_node)
        if self.head is None:
            new_node.next = new_node
            new_node.previous = new_node
            self.head = new_node
        else:
            self.insert_after(self.head.previous, new_node)

    def get_node(self, _index: int) -> Optional[GremlinScenarioNode]:
        if not isinstance(_index, int):
            error_msg: str = (
                f"get_node expects index as integer, received {type(_index)}"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        node: GremlinScenarioNode = self.head  # type: ignore
        for idx in range(_index):
            node = node.next
            if node == self.head:
                return None
        return node

    def insert_after(
        self, ref_node: GremlinScenarioNode, new_node: GremlinScenarioNode
    ) -> None:
        self._validate_type(new_node)
        new_node.previous = ref_node
        new_node.next = ref_node.next
        new_node.next.previous = new_node
        ref_node.next = new_node

    def insert_before(
        self, ref_node: GremlinScenarioNode, new_node: GremlinScenarioNode
    ) -> None:
        self._validate_type(new_node)
        self.insert_after(ref_node.previous, new_node)

    def next(self) -> None:
        self.head = self.head.next

    def nodes(self):
        if self.head is None:
            return
        node = self.head
        while True:
            yield node
            node = node.next
            if node == self.head:
                return

    def nodes_data_circular(self):
        for node in self.nodes():
            data = node.data
            yield node, data

    def nodes_data_linear(self):
        for node in self.nodes():
            data = node.data
            if node.next == self.head:
                data.pop("next")
            yield node, data

    def previous(self) -> None:
        self.head = self.head.previous

    def push(self, new_node: GremlinScenarioNode) -> None:
        self._validate_type(new_node)
        self.append(new_node)
        self.head = new_node

    def remove(self, _node: GremlinScenarioNode) -> None:
        if self.head.next == self.head:
            self.head = None  # type: ignore
        else:
            _node.previous.next = _node.next
            _node.next.previous = _node.previous
            if self.head == _node:
                self.head = _node.next

    @property
    def head(self) -> GremlinScenarioNode:
        if not self._head:
            return None  # type: ignore
        return self._head

    @head.setter
    def head(self, node: GremlinScenarioNode) -> None:
        self._validate_type(node)
        self._head = node

    def _validate_type(self, _node: GremlinScenarioNode) -> bool:
        _caller = inspect.stack()[2][3]
        if not issubclass(type(_node), GremlinScenarioNode):
            error_msg: str = f"{_caller} expects node to be a subclass of GremlinScenarioNode, received {type(_node)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        return True
