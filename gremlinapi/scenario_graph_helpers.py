# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import inspect
import json
import logging
import uuid
from typing import Union, Optional, Tuple

from gremlinapi.exceptions import (
    GremlinCommandTargetError,
    GremlinIdentifierError,
    GremlinParameterError,
)

from gremlinapi.attack_helpers import (
    GremlinAttackCommandHelper,
    GremlinAttackTargetHelper,
)
from gremlinapi.util import deprecated
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
        self._name: str = str()
        self._node_type: str = str()
        self.id: str = str(uuid.uuid4())
        self._index: str = str()
        self.index = "0"
        self._next: str = str()
        self.next = "0"
        self.name: str = kwargs.get("name", None)  # type: ignore

    def add_edge(self, _node: "GremlinScenarioNode", _weight: str = None) -> None:
        """
        Adds an edge from this node to the value of _node.

        This method contains the data structure for an edge.

        Parameters
        ----------
        _node : GremlinScenarioNode
            The node for which an edge needs to be added
        _weight : int optional
            The optional weight of the edge

        Raises
        ------
        GremlinParameterError
            If the _node is not of the type GremlinScenarioNode
        """
        if not issubclass(type(_node), GremlinScenarioNode):
            error_msg: str = (
                f"add_edge expects a GremlinScenarioNode, received {type(_node)}"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._edges[_node.id] = {"node": _node, "weight": _weight}

    @property
    def data(self) -> dict:
        return self.api_model()

    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, _id: str = None) -> None:
        if not isinstance(_id, str):
            error_msg: str = f"id expects a string {type(str)}, received {type(_id)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._id = _id

    @property
    def index(self) -> str:
        return self._index

    @index.setter
    def index(self, _index: str = "0") -> None:
        if not isinstance(_index, str):
            error_msg: str = (
                f"index expects an string {type(str)}, received {type(_index)}"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._index = _index

    @property
    def next(self) -> str:
        return self._next

    @next.setter
    def next(self, _next: str = "0") -> None:
        if not isinstance(_next, str):
            error_msg: str = (
                f"next expects an string {type(str)}, received {type(_next)}"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        self._next = _next

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
    def uuid(self) -> str:
        if not self.name:
            error_msg: str = f"Node Name is required to build a scenario node, please set a node name"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        return f"{self.name}-{self.id}"

    def api_model(self) -> dict:
        model = {
            "type": self.node_type,
            "guid": self.uuid,
            "id": self.index,
            "next": self.next,
        }
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["name"] = self.name
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


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

    def add_node(self, node: GremlinScenarioNode, _default_edge: bool = False) -> None:
        """
        Adds the node to the graph as a loose leaf. If it is the first node, it becomes the HEAD
        node.

        Parameters
        ----------
        node : GremlinScenarioNode
            The node to add to the graph
        _default_edge bool optional
            Adds an edge from node to the last-added node in the graph

        Raises
        ------
        GremlinParameterError
            If the node is not of the type GremlinScenarioNode
        """
        if not issubclass(type(node), GremlinScenarioNode):
            error_msg: str = (
                f"add_node expects GremlinScenarioNode (or None), received {type(node)}"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        if not self._nodes.head:
            _default_edge = False
        if _default_edge:
            tail_node = self._nodes._nodes[-1]
        self._nodes.append(node)
        if _default_edge:
            self.add_edge(node, tail_node)

    def remove_node(self, node: GremlinScenarioNode) -> None:
        """
        Removes node from graph.

        If the node to remove is the head node, Raises an error.

        Parameters
        ----------
        node : GremlinScenarioNode
            Node to remove from the graph

        Raises
        ------
        GremlinParameterError
            If the _node to remove is the current head node
        """
        self._nodes.remove(node)

    def get_last_node(self) -> GremlinScenarioNode:
        return self._nodes._nodes[-1]

    def add_edge(
        self,
        dst_node: GremlinScenarioNode,
        _src_node: GremlinScenarioNode = None,
        _weight: int = None,
    ) -> None:
        """
        Helper function to add edges to source and destination nodes, with optional weight.

        If _src_node is not defined, the node with the highest id (the last added)
        is used

        Parameters
        ----------
        dst_node : GremlinScenarioNode
            The node for which an edge needs to be added.
        _src_node : GremlinScenatioNode optional
            The optional source node if a custom edge is required.
        _weight : int optional
            The optional weight of the edge

        Raises
        ------
        GremlinParameterError
            If the _src_node or dst_node are not of the type GremlinScenarioNode
        """
        if not issubclass(type(dst_node), GremlinScenarioNode):
            error_msg: str = f"add_edge expects GremlinScenarioNode (or None), received {type(dst_node)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        if not _src_node:
            _src_node = self.get_last_node()
        self._nodes.add_edge(_src_node, dst_node, _weight)

    def remove_edge(
        self,
        src_node: GremlinScenarioNode,
        _edge_node: GremlinScenarioNode = None,
    ) -> None:
        """
        Helper function to remove edges from nodes

        If _edge_node is not defined, all edges from src_node will be removed from the graph

        Parameters
        ----------
        src_node : GremlinScenarioNode
            One side of the edge to be removed
        _edge_node : GremlinScenatioNode optional
            The optional other side of the edge to be removed

        Raises
        ------
        GremlinParameterError
            If src_node is not of the type GremlinScenarioNode
        """
        if not issubclass(type(src_node), GremlinScenarioNode):
            error_msg: str = f"remove_edge expects GremlinScenarioNode (or None), received {type(src_node)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)

        if not _edge_node:
            src_edges = src_node._edges.copy()
            for node_id in src_edges:
                self._nodes.remove_edge(src_node, src_node._edges[node_id]["node"])
        else:
            self._nodes.remove_edge(src_node, _edge_node)

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

    def api_model(self) -> dict:
        model: dict = {
            "description": self.description,
            "hypothesis": self.hypothesis,
            "name": self.name,
        }
        if self._nodes.head is not None:
            model["graph"] = {
                "start_id": "0",
                "nodes": self._nodes.get_nodes_linear()
                # "nodes": {
                #     node.uuid: data for node, data in self._nodes.nodes_data_linear()
                # }
            }
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["name"] = self.name
        kwargs["description"] = self.description
        kwargs["hypothesis"] = self.hypothesis
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


class GremlinScenarioSerialNode(GremlinScenarioNode):
    def __init(
        self,
        *args: tuple,
        **kwargs: dict,
    ):
        super().__init__(*args, **kwargs)

    def api_model(self) -> dict:
        model: dict = super().api_model()
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["name"] = self.name
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


class GremlinScenarioParallelNode(GremlinScenarioNode):
    def __init(
        self,
        *args: tuple,
        **kwargs: dict,
    ):
        super().__init__(*args, **kwargs)
        raise NotImplementedError("Parallel Scenario Nodes NOT IMPLEMENTED")

    def api_model(self) -> dict:
        model: dict = super().api_model()
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["name"] = self.name
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


class GremlinScenarioAttackNode(GremlinScenarioSerialNode):
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

    def api_model(self) -> dict:
        model: dict = super().api_model()
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["name"] = self.name
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


class GremlinScenarioILFINode(GremlinScenarioSerialNode):
    def __init__(self, *args: tuple, **kwargs: dict):
        if not kwargs.get("name", None) and kwargs.get("command", None):  # type: ignore
            kwargs["name"] = (kwargs.get("command")).shortType  # type: ignore
        super().__init__(*args, **kwargs)
        self._command: GremlinAttackCommandHelper = None  # type: ignore
        self._target: GremlinAttackTargetHelper = None  # type: ignore
        self.node_type: str = "InfraAttack"
        self.command: GremlinAttackCommandHelper = kwargs.get("command", GremlinAttackCommandHelper())  # type: ignore
        self.target: GremlinAttackTargetHelper = kwargs.get("target", GremlinAttackTargetHelper())  # type: ignore

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

    def api_model(self) -> dict:
        model: dict = super().api_model()
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

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["name"] = self.name
        kwargs["command"] = repr(self.command)
        kwargs["target"] = repr(self.target)
        return "%s(%s)" % (self.__class__.__name__, kwargs)

    def __str__(self) -> str:
        return repr(self)


class GremlinScenarioALFINode(GremlinScenarioSerialNode):
    def __init__(
        self,
        *args: tuple,
        **kwargs: dict,
    ):
        super().__init__(*args, **kwargs)
        self.attack_type = "ALFI"
        raise NotImplementedError("ALFI Scenarios NOT IMPLEMENTED")

    def api_model(self) -> dict:
        model: dict = super().api_model()
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["name"] = self.name
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


class GremlinScenarioDelayNode(GremlinScenarioSerialNode):
    def __init__(self, *args: tuple, **kwargs: dict):
        if not kwargs.get("name", None):
            kwargs["name"] = "Delay"  # type: ignore
        super().__init__(*args, **kwargs)
        self._delay: int = int()
        self._delay: int = kwargs.get("delay", None)  # type: ignore
        self.node_type: str = "Delay"

    def api_model(self) -> dict:
        model: dict = super().api_model()
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

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["name"] = self.name
        kwargs["delay"] = self.delay
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


class GremlinScenarioStatusCheckNode(GremlinScenarioSerialNode):
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

    def api_model(self) -> dict:
        model: dict = super().api_model()
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

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["name"] = self.name
        kwargs["description"] = self.description
        kwargs["endpoint_url"] = self.endpoint_url
        kwargs["endpoint_headers"] = self.endpoint_headers
        kwargs["evaluation_ok_status_codes"] = self.evaluation_ok_status_codes
        kwargs["evaluation_ok_latency_max"] = self.evaluation_ok_latency_max
        kwargs[
            "evaluation_response_body_evaluation"
        ] = self.evaluation_response_body_evaluation
        return "%s(%s)" % (self.__class__.__name__, json.dumps(kwargs))

    def __str__(self) -> str:
        return repr(self)


class _GremlinNodeGraph(object):
    def __init__(self):
        self._head: GremlinScenarioNode = None  # type: ignore
        self._nodes: list = []

    def add_edge(
        self,
        node_left: GremlinScenarioNode,
        node_right: GremlinScenarioNode,
        _weight=None,
    ) -> None:
        """
        Adds edges to left and right nodes, with optional weight

        Parameters
        ----------
        node_left : GremlinScenarioNode
            One side of the new edge
        node_right : GremlinScenarioNode
            One side of the new edge
        _weight : int optional
            The optional weight of the edge

        Raises
        ------
        GremlinParameterError
            If the node_left or node_right are not of the type GremlinScenarioNode
        """
        self._validate_type(node_left)
        self._validate_type(node_right)
        node_left.add_edge(node_right, _weight)
        node_right.add_edge(node_left, _weight)

    def remove_edge(
        self,
        node_left: GremlinScenarioNode,
        node_right: GremlinScenarioNode,
    ) -> None:
        """
        Removes edge to left and right nodes

        Parameters
        ----------
        node_left : GremlinScenarioNode
            One side of the edge
        node_right : GremlinScenarioNode
            One side of the edge

        Raises
        ------
        GremlinParameterError
            If the node_left or node_right are not of the type GremlinScenarioNode
        """
        self._validate_type(node_left)
        self._validate_type(node_right)
        node_left._edges.pop(node_right.id)
        node_right._edges.pop(node_left.id)

    def append(self, new_node: GremlinScenarioNode) -> None:
        """
        Adds new_node to the graph.

        Duplicates the functionality of list.append() and ensures the `head` node is set.

        Parameters
        ----------
        new_node : GremlinScenarioNode
            Node to add to the graph

        Raises
        ------
        GremlinParameterError
            If the new_node are not of the type GremlinScenarioNode
        """
        self._validate_type(new_node)
        if self.head is None:
            self.head = new_node
        self._nodes.append(new_node)

    def get_node(self, uid: str) -> Optional[GremlinScenarioNode]:
        """
        Retrieves the GremlinScenarioNode, if it exists, with id `id`

        Parameters
        ----------
        uid : str
            Node id to retrieve from graph
        """
        for node in self._nodes:
            if node.id == uid:
                return node
        return None

    def get_nodes_linear(
        self,
        node: GremlinScenarioNode = None,
        parent_id: str = None,
        next_index: int = 0,
    ) -> dict:
        """
        Retrieves all nodes, ordered by their defined edges.

        Only will work for a linear-defined graph (node -> node_2 -> node_3)

        Parameters
        ----------
        node : GremlinScenarioNode optional
            Optional root node from which to begin collecting ordered node list.
            Defaults to the `head` node if none is supplied.
        parent_id : str optional
            The trailing node id to be skipped when enumerating a node's edges.
            Prevents recursion loops
        next_index : int optional
            The next index to use
        """
        if not node:
            return self.get_nodes_linear(self.head)
        self._validate_type(node)
        node.index = str(next_index)
        node.next = str(next_index + 1)
        nodes: dict = {str(next_index): node.data}
        print(node.id)
        for node_id in node._edges:
            if node_id == parent_id:
                continue
            nodes.update(
                self.get_nodes_linear(
                    node._edges[node_id]["node"], node.id, next_index + 1
                )
            )
        return nodes

    def get_nodes_parallel(self):
        raise NotImplementedError("Parallel Scenario Nodes NOT IMPLEMENTED")

    def insert_between(
        self,
        node: GremlinScenarioNode,
        node_left: GremlinScenarioNode,
        node_right: GremlinScenarioNode,
    ) -> None:
        raise NotImplementedError("insert_between NOT IMPLEMENTED")

    def total_nodes(self) -> int:
        raise NotImplementedError("total_nodes NOT IMPLEMENTED")

    def longest_path(self) -> Tuple[str, str, int]:
        raise NotImplementedError("longest_path NOT IMPLEMENTED")

    @deprecated("Use add_edge instead")
    def insert_after(
        self, ref_node: GremlinScenarioNode, new_node: GremlinScenarioNode
    ) -> None:
        self._validate_type(new_node)
        self.add_edge(ref_node, new_node)

    @deprecated("Use add_edge instead")
    def insert_before(
        self, ref_node: GremlinScenarioNode, new_node: GremlinScenarioNode
    ) -> None:
        self._validate_type(new_node)
        self.add_edge(ref_node, new_node)

    @deprecated
    def nodes(self) -> list:
        return self._nodes

    @deprecated
    def nodes_data_circular(self):
        for node in self._nodes:
            data = node.data
            yield node, data

    @deprecated
    def nodes_data_linear(self):
        for node in self._nodes:
            data = node.data
            yield node, data

    @deprecated
    def previous(self) -> None:
        pass

    def push(self, new_node: GremlinScenarioNode) -> None:
        """
        Adds new_node to graph, replacing the `head` node

        Parameters
        ----------
        new_node : GremlinScenarioNode
            Node to add to the graph
        """
        self._validate_type(new_node)
        self.append(new_node)
        self.add_edge(new_node, self.head)
        self.head = new_node

    def remove(self, _node: GremlinScenarioNode) -> None:
        """
        Removes _node from graph.

        If the node to remove is the head node, Raises an error

        Parameters
        ----------
        _node : GremlinScenarioNode
            Node to remove from the graph

        Raises
        ------
        GremlinParameterError
            If the _node to remove is the current head node
        """
        if self.head == _node:
            error_msg: str = f"Node to remove cannot be the current head node"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        else:
            for node_id in _node._edges:
                _node._edges[node_id]["node"]._edges.pop(_node.id)
            _node._edges = {}
            self._nodes.remove(_node)

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

    def api_model(self) -> dict:
        model: dict = {}
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        return "%s()" % (self.__class__.__name__)

    def __str__(self) -> str:
        return repr(self)
