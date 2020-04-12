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

class GremlinScenarioHelper(object):
    def __init__(self, *args, **args):
        self._description = str()
        self._hypothesis = str()
        self._steps = []

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, _description=None):
        self._description = _description

    @property
    def hypothesis(self):
        return self._hypothesis

    @description.setter
    def hypothesis(self, _hypothesis=None):
        self._hypothesis = _hypothesis

    def __repr__(self):
        model = {
            'description': self.description,
            'hypothesis': self._hypothesis
        }
        return json.dumps(model)
