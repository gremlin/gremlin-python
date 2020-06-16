# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

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
        self._start = str()
        self.description = kwargs.get('description', None)
        self.hypothesis = kwargs.get('hypothesis', None)
        self.name = kwargs.get('start', None)

    def add_node(self, new_node=None):
        if not isinstance(new_node, GremlinScenarioNode):
            error_msg = f'add_node expects node to be a GremlinScenarioNode: {type(GremlinScenarioNode)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        if self.start is None:
            new_node.next = new_node
            new_node.previous = new_node
            self.start = new_node
        else:
            self.add_node_after(self.start.previous, new_node)

    def add_node_after(self, ref_node=None, new_node=None):
        if not isinstance(new_node, GremlinScenarioNode):
            error_msg = f'add_node expects node to be a GremlinScenarioNode: {type(GremlinScenarioNode)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        new_node.previous = ref_node
        new_node.next = ref_node.next
        new_node.next.previous = new_node
        ref_node.next = new_node

    def add_node_before(self, ref_node=None, new_node=None):
        self.add_node_after(ref_node.previous, new_node)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, description=None):
        if not isinstance(description, str):
            error_msg = f'Description expects string {type(str())}, received {type(description)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._description = description

    @property
    def hypothesis(self):
        return self._hypothesis

    @hypothesis.setter
    def hypothesis(self, hypothesis=None):
        if not isinstance(hypothesis, str):
            error_msg = f'Hypothesis expects string {type(str())}, received {type(hypothesis)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._hypothesis = hypothesis

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=None):
        if not isinstance(name, str):
            error_msg = f'Name expects string {type(str())}, received {type(name)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._name = name

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start=None):
        if not (isinstance(start, GremlinScenarioNode) or start is None):
            error_msg = f'Start expects GremlinScenarioNode (or None), received {type(start)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._name = start


class GremlinScenarioNode(object):
    def __init__(self, *args, **kwargs):
        self._edges = list()
        self._id = str()
        self._previous = None
        self._name = str()
        self._next = None
        self._node_type = str()
        self.id = str(uuid.uuid4())

    def add_edge(self, new_node=None):
        self._edges.append(new_node)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id=None):
        if not isinstance(id, str):
            error_msg = f''
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._id = id

    @property
    def previous(self):
        return self._previous

    @previous.setter
    def previous(self, new_node=None):
        if not (isinstance(new_node, GremlinScenarioNode) or new_node is None):
            error_msg = f'previous expects GremlinScenarioNode (or None), received {type(new_node)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._previous = new_node

    @property
    def next(self):
        return self._next

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name=None):
        if not isinstance(name, str):
            error_msg = f'name expects type string {type(str)}, received {type(name)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._name = name

    @next.setter
    def next(self, new_node):
        if not (isinstance(new_node, GremlinScenarioNode) or new_node is None):
            error_msg = f'next expects GremlinScenarioNode (or None), received {type(new_node)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._previous = new_node

    @property
    def node_type(self):
        return self._node_type

    @node_type.setter
    def node_type(self, node_type=None):
        if not isinstance(node_type, str):
            error_msg = f'node_type expects string {type(str)}, received {type(node_type)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._node_type = node_type


class GremlinScenarioAttackNode(GremlinScenarioNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._attack_type = str()

    @property
    def attack_type(self):
        return self._attack_type

    @attack_type.setter
    def attack_type(self, attack_type=None):
        if not isinstance(attack_type, str):
            error_msg = f'attack_type expects string {type(str)}, received {type(attack_type)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        self._attack_type = attack_type


class GremlinScenarioILFINode(GremlinScenarioAttackNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack_type = "ILFI"


class GremlinScenarioALFINode(GremlinScenarioAttackNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.attack_type = "ALFI"


class GremlinScenarioDelayNode(GremlinScenarioNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.node_type = "wait"


class GremlinScenarioStatusCheckNode(GremlinScenarioNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.node_type = "status-check"

