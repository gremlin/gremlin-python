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


class GremlinScenarioHelper(object):
    def __init__(self, *args, **kwargs):
        self._description = str()
        self._hypothesis = str()
        self._name = str()
        self._steps = list()
        self.description = kwargs.get('description', self._description)
        self.hypothesis = kwargs.get('hypothesis', self._hypothesis)
        self.name = kwargs.get('name', self._name)

    def add_step(self, _step=None):
        if not issubclass(type(_step), GremlinScenarioStep):
            error_msg = f'The step must extend from {type(GremlinScenarioStep)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        _cur_step_obj = json.loads(str(_step))
        if len(self._steps) > 0:
            log.debug('checking last step')
            _last_step_obj = self._steps[-1]
            last_attack_type = _last_step_obj['attacks'][0]['attackType']
            last_target_type = _last_step_obj['attacks'][0]['targetDefinition']['targetType']
            last_command_type = _last_step_obj['attacks'][0]['impactDefinition']['commandType']
            cur_attack_type = _cur_step_obj['attacks'][0]['attackType']
            cur_target_type = _cur_step_obj['attacks'][0]['targetDefinition']['targetType']
            cur_command_type = _cur_step_obj['attacks'][0]['impactDefinition']['commandType']
            if not last_attack_type == cur_attack_type:
                error_msg = f'Each step must target the same attackType'
                log.fatal(error_msg)
                raise GremlinCommandTargetError(error_msg)
            if not last_target_type == cur_target_type:
                error_msg = f'Each step must target the same primitive typeset'
                log.fatal(error_msg)
                raise GremlinCommandTargetError(error_msg)
            if not last_command_type == cur_command_type:
                error_msg = f'Each step must use the same command type'
                log.fatal(error_msg)
                raise GremlinCommandTargetError(error_msg)
            self._steps.append(_cur_step_obj)
        else:
            log.debug('fist step, just adding')
            self._steps.append(_cur_step_obj)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, _description=None):
        self._description = _description

    @property
    def hypothesis(self):
        return self._hypothesis

    @hypothesis.setter
    def hypothesis(self, _hypothesis=None):
        self._hypothesis = _hypothesis

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, _name=None):
        if isinstance(_name, str):
            self._name = _name
        else:
            error_msg = f'name expects type {type(str)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)

    @property
    def steps(self):
        return self._steps

    @steps.setter
    def steps(self, _steps=None):
        error_msg = f'Interface not implemented, use `add_step`'
        log.warning(error_msg)
        raise NotImplemented(error_msg)

    def __repr__(self):
        model = {
            'description': self.description,
            'hypothesis': self.hypothesis,
            'name': self.name,
            'steps': self.steps
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
        model = {
            'delay': self.delay
        }
        return json.dumps(model)


class GremlinILFIStep(GremlinScenarioStep):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._command = None
        self._target = None
        self.command = kwargs.get('command', self._command)
        self.target = kwargs.get('target', self._target)

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, _command=None):
        if _command and issubclass(type(_command), GremlinAttackCommandHelper):
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
        if _target and issubclass(type(_target), GremlinAttackTargetHelper):
            self._target = _target
        else:
            error_msg = f'target expects a GremlinAttackTargetHelper {type(GremlinAttackTargetHelper)}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)

    def __repr__(self):
        model = json.loads(super().__repr__())
        model['attacks'] = [{
            'attackType': 'ILFI',
            'impactDefinition': self.command.impact_definition(),
            'targetDefinition': self.target.target_definition()
        }]
        model['id'] = str(uuid.uuid3(uuid.NAMESPACE_X500, str(model['attacks'])))
        return json.dumps(model)


class GremlinALFIStep(GremlinScenarioStep):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        error_msg = f'GremlinALFIStep NOT IMPLEMENTED'
        log.fatal(error_msg)
        raise NotImplemented(error_msg)

    def __repr__(self):
        model = json.loads(super().__repr__())
        return json.dumps(model)

