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

from gremlinapi.attack_helpers import GremlinAttackCommandHelper, GremlinAttackTargetHelper
from gremlinapi.clients import GremlinAPIClients as clients
from gremlinapi.containers import GremlinAPIContainers as containers
from gremlinapi.providers import GremlinAPIProviders as providers

log = logging.getLogger('GremlinAPI.client')


class GremlinScenarioHelper(object):
    def __init__(self, *args, **kwargs):
        self._description = str()
        self._hypothesis = str()
        self._steps = list()
        self.description = kwargs.get('description', self._description)
        self.hypothesis = kwargs.get('hypothesis', self._hypothesis)

    def add_step(self, *args, **kwargs):
        _step = kwargs.get('step', None)
        if not issubclass(_step, GremlinScenarioStep):
            error_msg = f'The step must extend from {type(GremlinScenarioStep)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)

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


class GremlinScenarioStep(object):
    def __init__(self, *args, **kwargs):
        self._delay = 5
        self.delay = kwargs.get('delay', self._delay)

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, _delay):
        if isinstance(_delay, int) and _delay >= 1:
            self._delay = _delay
        else:
            error_msg = f'delay expects a positive integer {type(int)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)

    def __repr__(self):
        model = dict()
        return json.dumps(model)


class GremlinILFIStep(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._command = None
        self._target = None
        self.command = kwargs.get('command', None)
        self.target = kwargs.get('target', None)

    def _coherce_command(self):
        atk_model = json.loads(str(self._command))
        _model = {

        }
        return _model

    def _coherce_target(self):
        tgt_model = json.loads(str(self._target))
        _model = {

        }
        return _model

    def _make_scenario_step(self):
        _model = {
            'attackType': 'ILFI',
            'impactDefinition': self._coherce_command(),
            'targetDefinition': self._coherce_target(),
        }
        return _model

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, _command=None):
        if _command and issubclass(_command, GremlinAttackCommandHelper):
            self._command = _command
        else:
            error_msg = f'command expects a GremlinAttackCommandHelper {type(GremlinAttackCommandHelper)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, _target=None):
        if _target and issubclass(_target, GremlinAttackTargetHelper):
            self._target = _target
        else:
            error_msg = f'target expects a GremlinAttackTargetHelper {type(GremlinAttackTargetHelper)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)

    def __repr__(self):
        model = json.loads(super().__repr__())
        return json.dumps(model)


class GremlinALFIStep(object):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        error_msg = f'GremlinALFIStep NOT IMPLEMENTED'
        log.fatal(error_msg)
        raise NotImplemented(error_msg)

    def __repr__(self):
        model = json.loads(super().__repr__())

        return json.dumps(model)

