# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import json
import logging
import uuid

from gremlinapi.util import deprecated
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

log = logging.getLogger("GremlinAPI.client")


class GremlinScenarioHelper(object):
    @deprecated(
        "GremlinScenarioHelper class is deprecated, plesae use GremlinScenarioGraphHelper instead"
    )
    def __init__(
        self,
        *args: tuple,
        **kwargs: dict,
    ):
        self._description: str = str()
        self._hypothesis: str = str()
        self._name: str = str()
        self._steps: list = list()
        self.description: str = kwargs.get("description", self._description)  # type: ignore
        self.hypothesis: str = kwargs.get("hypothesis", self._hypothesis)  # type: ignore
        self.name: str = kwargs.get("name", self._name)  # type: ignore

    @deprecated(
        "GremlinScenarioHelper class is deprecated, plesae use GremlinScenarioGraphHelper instead"
    )
    def add_step(self, _step: "GremlinScenarioStep") -> None:
        if not issubclass(type(_step), GremlinScenarioStep):
            error_msg: str = f"The step must extend from {type(GremlinScenarioStep)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        _cur_step_obj: dict = json.loads(str(_step))
        if len(self._steps) > 0:
            if log.getEffectiveLevel() == logging.DEBUG:
                log.debug("checking last step")
            _last_step_obj: dict = self._steps[-1]
            last_attack_type: str = _last_step_obj["attacks"][0]["attackType"]
            last_target_type: str = _last_step_obj["attacks"][0]["targetDefinition"][
                "strategyType"
            ]
            last_command_type: str = _last_step_obj["attacks"][0]["impactDefinition"][
                "commandType"
            ]
            cur_attack_type: str = _cur_step_obj["attacks"][0]["attackType"]
            cur_target_type: str = _cur_step_obj["attacks"][0]["targetDefinition"][
                "strategyType"
            ]
            cur_command_type: str = _cur_step_obj["attacks"][0]["impactDefinition"][
                "commandType"
            ]
            if not last_attack_type == cur_attack_type:
                error_msg = f"Each step must target the same attackType"
                log.error(error_msg)
                raise GremlinCommandTargetError(error_msg)
            if not last_target_type == cur_target_type:
                error_msg = f"Each step must target the same primitive typeset"
                log.error(error_msg)
                raise GremlinCommandTargetError(error_msg)
            if not last_command_type == cur_command_type:
                error_msg = f"Each step must use the same command type"
                log.error(error_msg)
                raise GremlinCommandTargetError(error_msg)
            self._steps.append(_cur_step_obj)
        else:
            if log.getEffectiveLevel() == logging.DEBUG:
                log.debug("fist step, just adding")
            self._steps.append(_cur_step_obj)

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, _description: str = "") -> None:
        self._description = _description

    @property
    def hypothesis(self) -> str:
        return self._hypothesis

    @hypothesis.setter
    def hypothesis(self, _hypothesis: str = "") -> None:
        self._hypothesis = _hypothesis

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, _name: str = None) -> None:
        if isinstance(_name, str):
            self._name = _name
        else:
            error_msg: str = f"name expects type {type(str)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)

    @property
    def steps(self) -> list:
        return self._steps

    @steps.setter
    def steps(self, _steps=None) -> None:
        error_msg = f"Interface not implemented, use `add_step`"
        log.warning(error_msg)
        raise NotImplementedError(error_msg)

    @deprecated(
        "GremlinScenarioHelper class is deprecated, plesae use GremlinScenarioGraphHelper instead"
    )
    def __repr__(self) -> str:
        model: dict = {
            "description": self.description,
            "hypothesis": self.hypothesis,
            "name": self.name,
            "steps": self.steps,
        }
        return json.dumps(model)


class GremlinScenarioStep(object):
    @deprecated(
        "GremlinScenarioStep class is deprecated, plesae use GremlinScenarioGraphHelper instead"
    )
    def __init__(
        self,
        *args: tuple,
        **kwargs: dict,
    ):
        self._delay: int = 5
        self.delay: int = kwargs.get("delay", self._delay)  # type: ignore

    @property
    def delay(self) -> int:
        return self._delay

    @delay.setter
    def delay(self, _delay: int) -> None:
        if isinstance(_delay, int) and _delay >= 1:
            self._delay = _delay
        else:
            error_msg: str = f"delay expects a positive integer {type(int)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)

    @deprecated(
        "GremlinScenarioStep class is deprecated, plesae use GremlinScenarioGraphHelper instead"
    )
    def __repr__(self) -> str:
        model: dict = {"delay": self.delay}
        return json.dumps(model)


class GremlinILFIStep(GremlinScenarioStep):
    @deprecated(
        "GremlinILFIStep class is deprecated, plesae use GremlinScenarioGraphHelper instead"
    )
    def __init__(
        self,
        *args: tuple,
        **kwargs: dict,
    ):
        super().__init__(*args, **kwargs)
        self._command: GremlinAttackCommandHelper = None  # type: ignore
        self._target: GremlinAttackTargetHelper = None  # type: ignore
        self.command: GremlinAttackCommandHelper = kwargs.get("command", self._command)  # type: ignore
        self.target: GremlinAttackTargetHelper = kwargs.get("target", self._target)  # type: ignore

    @property
    def command(self) -> GremlinAttackCommandHelper:
        return self._command

    @command.setter
    def command(self, _command: GremlinAttackCommandHelper = None) -> None:
        if _command and issubclass(type(_command), GremlinAttackCommandHelper):
            self._command = _command
        else:
            error_msg: str = f"command expects a GremlinAttackCommandHelper {type(GremlinAttackCommandHelper)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)

    @property
    def target(self) -> GremlinAttackTargetHelper:
        return self._target

    @target.setter
    def target(self, _target: GremlinAttackTargetHelper = None) -> None:
        if _target and issubclass(type(_target), GremlinAttackTargetHelper):
            self._target = _target
        else:
            error_msg: str = f"target expects a GremlinAttackTargetHelper {type(GremlinAttackTargetHelper)}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)

    @deprecated(
        "GremlinILFIStep class is deprecated, plesae use GremlinScenarioGraphHelper instead"
    )
    def __repr__(self) -> str:
        model: dict = json.loads(super().__repr__())
        model["attacks"] = [
            {
                "attackType": "ILFI",
                "impactDefinition": self.command.impact_definition(),
                "targetDefinition": self.target.target_definition(),
            }
        ]
        model["id"] = str(uuid.uuid3(uuid.NAMESPACE_X500, str(model["attacks"])))
        return json.dumps(model)


class GremlinALFIStep(GremlinScenarioStep):
    @deprecated(
        "GremlinALFIStep class is deprecated, plesae use GremlinScenarioGraphHelper instead"
    )
    def __init__(
        self,
        *args: tuple,
        **kwargs: dict,
    ):
        super().__init__(*args, **kwargs)
        error_msg: str = f"GremlinALFIStep NOT IMPLEMENTED"
        log.error(error_msg)
        raise NotImplementedError(error_msg)

    @deprecated(
        "GremlinALFIStep class is deprecated, plesae use GremlinScenarioGraphHelper instead"
    )
    def __repr__(self) -> str:
        model: dict = json.loads(super().__repr__())
        return json.dumps(model)
