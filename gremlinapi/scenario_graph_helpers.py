# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import inspect
import json
import logging
import uuid

from gremlinapi.exceptions import (
    GremlinCommandTargetError,
    GremlinIdentifierError,
    GremlinParameterError
)

from gremlinapi.attack_helpers import GremlinAttackCommandHelper, GremlinAttackTargetHelper
from gremlinapi.clients import GremlinAPIClients as clients
from gremlinapi.containers import GremlinAPIContainers as containers
from gremlinapi.providers import GremlinAPIProviders as providers

log = logging.getLogger('GremlinAPI.client')

class GremlinScenarioGraphHelper(object):
    def __init__(self, *args, **kwargs):
        self._description = str()
        self._hypothesis = str()
        self._name = str()
        self._nodes = _GremlinNodeGraph()
        self._start = str()
        self.description = kwargs.get('description', None)
        self.hypothesis = kwargs.get('hypothesis', None)
        self.name = kwargs.get('name', None)

    def add_node(self, _node=None):
        if not issubclass(type(_node), GremlinScenarioNode):
            error_msg = f'add_node expects GremlinScenarioNode (or None), received {type(_node)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._nodes.append(_node)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, _description=None):
        if not isinstance(_description, str):
            error_msg = f'Description expects string {type(str())}, received {type(_description)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._description = _description

    @property
    def hypothesis(self):
        return self._hypothesis

    @hypothesis.setter
    def hypothesis(self, _hypothesis=None):
        if not isinstance(_hypothesis, str):
            error_msg = f'Hypothesis expects string {type(str())}, received {type(_hypothesis)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._hypothesis = _hypothesis

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, _name=None):
        if not isinstance(_name, str):
            error_msg = f'Name expects string {type(str())}, received {type(_name)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._name = _name

    def repr_model(self):
        model = {
            'description': self.description,
            'hypothesis': self.hypothesis,
            'name': self.name
        }
        if self._nodes.head is not None:
            model['graph'] = {
                'start_id': self._nodes.head.uuid,
                'nodes': {node.uuid: data for node, data in self._nodes.nodes_data_linear()}
            }
        return model

    def __repr__(self):
        model = self.repr_model()
        return json.dumps(model)


class GremlinScenarioNode(object):
    def __init__(self, *args, **kwargs):
        self._edges = dict()
        self._id = str()
        self._previous = None
        self._name = str()
        self._next = None
        self._node_type = str()
        self.id = str(uuid.uuid4())
        self.name = kwargs.get('name', None)

    def add_edge(self, _node=None, _weight=None):
        if not issubclass(type(_node), GremlinScenarioNode):
            error_msg = f'add_edge expects a GremlinScenarioNode, received {type(_node)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._edges[_node.id] = {'node': _node, 'weight': _weight}

    @property
    def data(self):
        return self.repr_model()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, _id=None):
        if not isinstance(_id, str):
            error_msg = f'id expects a string {type(str)}, received {type(str)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._id = _id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, _name=None):
        if not isinstance(_name, str):
            error_msg = f'name expects type string {type(str)}, received {type(_name)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._name = _name

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, _node=None):
        if not issubclass(type(_node), GremlinScenarioNode):
            error_msg = f'next expects a GremlinScenarioNode, received {type(_node)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._next = _node

    @property
    def node_type(self):
        return self._node_type

    @node_type.setter
    def node_type(self, _node_type=None):
        if not isinstance(_node_type, str):
            error_msg = f'node_type expects string {type(str)}, received {type(_node_type)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._node_type = _node_type

    @property
    def previous(self):
        return self._previous

    @previous.setter
    def previous(self, _node=None):
        if not issubclass(type(_node), GremlinScenarioNode):
            error_msg = f'previous expects a GremlinScenarioNode, received {type(_node)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._previous = _node

    @property
    def uuid(self):
        if not self.name:
            error_msg = f'Node Name is required to build a scenario node, please set a node name'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        return f'{self.name}-{self.id}'

    def repr_model(self):
        model = {
            'type': self.node_type,
            'id': self.uuid,
            'next': self.next.uuid
        }
        return model

    def __repr__(self):
        return json.dumps(self.repr_model)


class GremlinScenarioAttackNode(GremlinScenarioNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.node_type = "attack"
        self._attack_type = str()

    @property
    def attack_type(self):
        return self._attack_type

    @attack_type.setter
    def attack_type(self, _attack_type=None):
        if not isinstance(_attack_type, str):
            error_msg = f'attack_type expects string {type(str)}, received {type(_attack_type)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._attack_type = _attack_type


class GremlinScenarioILFINode(GremlinScenarioAttackNode):
    def __init__(self, *args, **kwargs):
        if not kwargs.get('name', None) and kwargs.get('command', None):
            kwargs['name'] = kwargs.get('command').shortType
        super().__init__(*args, **kwargs)
        self._command = None
        self._target = None
        self.node_type = "InfraAttack"
        self.command = kwargs.get('command', self._command)
        self.target = kwargs.get('target', self._target)

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, _command=None):
        if not issubclass(type(_command), GremlinAttackCommandHelper):
            error_msg = f'impact_definition expects a GremlinAttackCommandHelper, received {type(_command)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._command = _command

    def repr_model(self):
        model = super().repr_model()
        model['impact_definition'] = self.command.impact_definition_graph()
        model['target_definition'] = self.target.target_definition_graph()
        return model

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, _target=None):
        if not issubclass(type(_target), GremlinAttackTargetHelper):
            error_msg = f'target_definition expects a GremlinAttackTargetHelper, received {type(_target)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._target = _target


class GremlinScenarioALFINode(GremlinScenarioAttackNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack_type = "ALFI"
        raise NotImplementedError('ALFI Scenarios NOT IMPLEMENTED')


class GremlinScenarioDelayNode(GremlinScenarioNode):
    def __init__(self, *args, **kwargs):
        if not kwargs.get('name', None):
            kwargs['name'] = 'Delay'
        super().__init__(*args, **kwargs)
        self._delay = int()
        self._delay = kwargs.get('delay', None)
        self.node_type = "Delay"

    def repr_model(self):
        model = super().repr_model()
        model['delay'] = self.delay
        return model

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, _duration=None):
        if not isinstance(_duration, int):
            error_msg = f'delay expects int type {type(int)}, received {type(_duration)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._delay = _duration


class GremlinScenarioStatusCheckNode(GremlinScenarioNode):
    def __init__(self, *args, **kwargs):
        if not kwargs.get('name', None):
            kwargs['name'] = 'status-check'
        super().__init__(*args, **kwargs)
        self.node_type = "SynchronousStatusCheck"
        self._description = str()
        self._endpoint_url = str()
        self._endpoint_headers = None
        self._evaluation_ok_status_codes = list()
        self._evaluation_ok_latency_max = int()
        self._evaluation_response_body_evaluation = None
        self.description = kwargs.get('description', None)
        self.endpoint_url = kwargs.get('endpoint_url', None)
        self.endpoint_headers = kwargs.get('endpoint_headers', None)
        self.evaluation_ok_status_codes = kwargs.get('evaluation_ok_status_codes', ["200-203"])
        self.evaluation_ok_latency_max = kwargs.get('evaluation_ok_latency_max', 500)
        self.evaluation_response_body_evaluation = kwargs.get('evaluation_response_body_evaluation', "")

    def repr_model(self):
        model = super().repr_model()
        model['endpointConfiguration'] = {
            'url': self.endpoint_url,
            'headers': self.endpoint_headers
        }
        model['evaluationConfiguration'] = {
            'okStatusCodes': self.evaluation_ok_status_codes,
            'okLatencyMaxMs': self.evaluation_ok_latency_max,
            'responseBodyEvaluation': self.evaluation_response_body_evaluation
        }
        model['thirdPartyPresets'] = 'PythonSDK'
        return model

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, _description=None):
        if not isinstance(_description, str):
            error_msg = f'description expects string, received {type(_description)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._description = _description

    @property
    def endpoint_headers(self):
        return self._endpoint_headers

    @endpoint_headers.setter
    def endpoint_headers(self, _headers=None):
        self._endpoint_headers = _headers

    @property
    def endpoint_url(self):
        return self._endpoint_url

    @endpoint_url.setter
    def endpoint_url(self, _url=None):
        if not isinstance(_url, str):
            error_msg = f'url expects a valid url string, received {type(_url)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._endpoint_url = _url

    @property
    def evaluation_ok_status_codes(self):
        return self._evaluation_ok_status_codes

    @evaluation_ok_status_codes.setter
    def evaluation_ok_status_codes(self, _status_codes=None):
        if not isinstance(_status_codes, list):
            error_msg = f'evaluation_ok_status_codes expects a list of integers or strings, received {type(_status_codes)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._evaluation_ok_status_codes = _status_codes

    @property
    def evaluation_ok_latency_max(self):
        return self._evaluation_ok_latency_max

    @evaluation_ok_latency_max.setter
    def evaluation_ok_latency_max(self, _latency=None):
        if not isinstance(_latency, int):
            error_msg = f'evaluation_ok_latency_max expects an int, received {type(_latency)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._evaluation_ok_latency_max = _latency

    @property
    def evaluation_response_body_evaluation(self):
        return self._evaluation_response_body_evaluation

    @evaluation_response_body_evaluation.setter
    def evaluation_response_body_evaluation(self, _evaluation_response_body_evaluation=None):
        if not _evaluation_response_body_evaluation:
            error_msg = f'evaluation_response_body_evaluation expects an argument, none provided'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._evaluation_response_body_evaluation = _evaluation_response_body_evaluation


class _GremlinNodeGraph(object):
    def __init__(self):
        self._head = None

    def add_edge(self, src_node=None, dest_node=None, _weight=None):
        self._validate_type(src_node)
        self._validate_type(dest_node)
        src_node.add_edge(dest_node, _weight)
        dest_node.add_edge(src_node, _weight)

    def append(self, new_node=None):
        self._validate_type(new_node)
        if self.head is None:
            new_node.next = new_node
            new_node.previous = new_node
            self.head = new_node
        else:
            self.insert_after(self.head.previous, new_node)

    def get_node(self, _index=None):
        if not isinstance(_index, int):
            error_msg = f'get_node expects index as integer, received {type(_index)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        node = self.head
        for idx in range(_index):
            node = node.next
            if node == self.head:
                return None
        return node

    def insert_after(self, ref_node=None, new_node=None):
        self._validate_type(new_node)
        new_node.previous = ref_node
        new_node.next = ref_node.next
        new_node.next.previous = new_node
        ref_node.next = new_node

    def insert_before(self, ref_node=None, new_node=None):
        self._validate_type(new_node)
        self.insert_after(ref_node.previous, new_node)

    def next(self):
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
                data.pop('next')
            yield node, data

    def previous(self):
        self.head = self.head.previous

    def push(self, new_node=None):
        self._validate_type(new_node)
        self.append(new_node)
        self.head = new_node

    def remove(self, _node=None):
        if self.head.next == self.head:
            self.head = None
        else:
            _node.previous.next = _node.next
            _node.next.previous = _node.previous
            if self.head == node:
                self.head = node.next

    @property
    def head(self):
        if not self._head:
            return None
        return self._head

    @head.setter
    def head(self, node=None):
        self._validate_type(node)
        self._head = node

    def _validate_type(self, _node=None):
        _caller = inspect.stack()[2][3]
        if not issubclass(type(_node), GremlinScenarioNode):
            error_msg = f'{_caller} expects node to be a subclass of GremlinScenarioNode, received {type(_node)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        return True

