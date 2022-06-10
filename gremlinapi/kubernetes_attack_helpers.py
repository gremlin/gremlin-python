import json
import logging
import re
import pprint

from gremlinapi.exceptions import (
    GremlinCommandTargetError,
    GremlinIdentifierError,
    GremlinParameterError
)

from typing import Type, Optional, Union, Dict, Any, Pattern

from gremlinapi.clients import GremlinAPIClients as clients
from gremlinapi.containers import GremlinAPIContainers as containers
from gremlinapi.providers import GremlinAPIProviders as providers
from gremlinapi.kubernetes import GremlinAPIKubernetesTargets as kubernetes_targets
from gremlinapi.attack_helpers import GremlinAttackTargetHelper, GremlinAttackHelper


log = logging.getLogger("GremlinAPI.client")


class GremlinKubernetesAttackTarget(object):
    '''
    A single k8s attack target in Gremlin.
    This can be a pod, replicaset, statefulset, deployment or daemonset.
    User must provide all attributes except for uid.
        uid will be retrieved automagically
    '''

    def __init__(self, *args: tuple, **kwargs: dict):
        self._cluster_id: str = ""
        self._namespace: str = ""
        self._allowed_kinds: list = [
            "DAEMONSET",
            "DEPLOYMENT",
            "POD",
            "REPLICASET",
            "STATEFULSET"
        ]
        self._kind: str = ""
        self._name: str = ""
        self._cluster_id: str = ""
        self._uid: str = ""

        # Setting values using setter
        self.cluster_id = (kwargs.get("cluster_id", self._cluster_id))
        self.namespace = (kwargs.get("namespace", self._namespace))
        self.kind = (kwargs.get("kind", self._kind))
        self.name = (kwargs.get("name", self._name))

        # Setting uid will perform all validation required.
        self.__set_uid()

    @property
    def cluster_id(self) -> str:
        return self._cluster_id

    @cluster_id.setter
    def cluster_id(self, _cluster_id: str = None) -> None:
        if isinstance(_cluster_id, str) and _cluster_id:
            self._cluster_id = _cluster_id
        else:
            error_msg: str = (
                f"Cluster ID cannot be empty"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)

    @property
    def namespace(self) -> str:
        return self._namespace

    @namespace.setter
    def namespace(self, _namespace: str = None) -> None:
        if isinstance(_namespace, str) and _namespace:
            self._namespace = _namespace
        else:
            error_msg: str = (
                f"Namespace cannot be empty"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)

    @property
    def kind(self) -> str:
        return self._kind

    @kind.setter
    def kind(self, _kind: str = None) -> None:
        if isinstance(_kind, str) and _kind.upper() in self._allowed_kinds:
            self._kind = _kind.upper()
        elif not _kind:
            allowed_kinds_str = str(self._allowed_kinds)
            error_msg: str = (
                f"kind must be set. Valid values {allowed_kinds_str}"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, _name: str = None) -> None:
        if isinstance(_name, str) and _name:
            self._name = _name
        else:
            error_msg: str = (
                f"Name cannot be empty"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)

    def __set_uid(self) -> None:
        '''
        Pull all targets and refine to exactly a single target.
        Otherwise throw an error
        '''

        target_objects = []
        all_objects = kubernetes_targets.list_kubernetes_targets()
        for cluster in all_objects:

            # Targets are exposed as a list of json objects.
            # Each json object is a k8s cluster and all associated
            #   k8s objects inside a list called "objects"
            if cluster['clusterId'] != self._cluster_id:
                continue

            for object in cluster['objects']:

                if object['kind'] != self._kind:
                    continue
                elif object['namespace'] != self._namespace:
                    continue
                elif object['name'] != self._name:
                    continue
                target_objects.append(object)

            break

        if len(target_objects) != 1:
            target_object_len = len(target_objects)
            error_msg: str = (
                f"""Exactly one target should be identified by target filter.
                {target_object_len} were idenfied by these filters:
                 kind: {self._kind}
                 clusterId: {self._cluster_id}
                 namespace: {self._namespace}
                 name: {self._name}"""
            )
            log.error(error_msg)
            raise GremlinIdentifierError(error_msg)

        self._uid = target_objects[0]['uid']

    def api_model(self) -> dict:
        model: dict = {
            "clusterId": self._cluster_id,
            "namespace": self._namespace,
            "kind": self._kind,
            "name": self._name,
            "uid": self._uid
        }
        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["clusterId"] = self._cluster_id,
        kwargs["namespace"] = self._namespace,
        kwargs["kind"] = self._kind,
        kwargs["name"] = self._name,
        kwargs["uid"] = self._uid
        return "%s(%s)" % (self.__class__.__name__, kwargs)

    def __str__(self) -> str:
        return repr(self)


class GremlinKubernetesAttackTargetHelper(GremlinAttackTargetHelper):
    '''
    '''

    def __init__(self, *args: tuple, **kwargs: dict):
        '''
        Provide a list of target objects
        Specify either percentage or count. Not both.
        '''
        self._targets = []
        self._percentage = None
        self._count = None

        self.targets = kwargs.get("targets", [])

        # count and percentage should not be
        if kwargs.get("count", None) and kwargs.get("percentage", None):
            error_msg: str = (
                f"Exactly one of `count` or `percentage` should be specified. Values were given for both settings."
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        elif not (kwargs.get("count", None) or kwargs.get("percentage", None)):
            error_msg: str = (
                f"Exactly one of `count` or `percentage` should be specified."
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)

        self.count = kwargs.get("count", None)
        self.percentage = kwargs.get("percentage", None)

    def target_definition(self) -> dict:
        model: dict = self.api_model()
        _target_definition: dict = {
            "strategy": {
                "k8sObjects": model['targets']
            }
        }

        if 'count' in model and model['count']:
            _target_definition['strategy']['count'] = model['count']
        elif 'percentage' in model and model['percentage']:
            _target_definition['strategy']['percentage'] = model['percentage']

        return _target_definition

    def target_definition_graph(self) -> dict:
        model: dict = self.api_model()
        _target_definition: dict = {
            'strategy': {},
            "strategy_type": "Random",
            "target_type": "Kubernetes",
            "k8s_objects": model['targets']
        }
        if 'count' in model and model['count']:
            _target_definition['strategy']['type'] = 'RandomCount'
            _target_definition['strategy']['count'] = model['count']
        elif 'percentage' in model and model['percentage']:
            _target_definition['strategy']['type'] = 'RandomPercent'
            _target_definition['strategy']['percentage'] = model['percentage']

        return _target_definition

    @property
    def targets(self) -> list:
        return self._targets

    @targets.setter
    def targets(self, _targets: list = []) -> None:
        if len(_targets) > 0:
            self._targets = _targets
        else:
            targets_len = len(_targets)
            error_msg: str = (
                f"""`targets` must be a non-empty list of type GremlinKubernetesAttackTarget.
                Given list was ({targets_len}) in length."""
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)

    @property
    def percentage(self) -> int:
        return self._percentage

    @percentage.setter
    def percentage(self, _percentage) -> None:
        if not _percentage:
            self._percentage = None
        elif _percentage <= 0 or _percentage > 100:
            error_msg: str = (
                f"Percentage must be an integer between 1 and 100. Given value ({_percentage})"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        else:
            self._percentage = _percentage
            self._count = None

    @property
    def count(self) -> int:
        return self._count

    @count.setter
    def count(self, _count) -> None:
        if not _count:
            self._count = None
        elif _count <= 0:
            error_msg: str = (
                f"Count should be a non-zero integer. Given value ({_count})"
            )
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        else:
            self._count = _count
            self._percentage = None

    def api_model(self) -> dict:
        model: dict = {
            "targets": [target.api_model() for target in self._targets],
        }
        if self._count:
            model['count'] = self._count
        elif self._percentage:
            model['percentage'] = self._percentage

        return model

    def __repr__(self) -> str:
        kwargs: dict = {}
        kwargs["targets"] = [repr(target) for target in self._targets]
        if self._count:
            kwargs['count'] = self._count
        elif self._percentage:
            kwargs['percentage'] = self._percentage
        return "%s(%s)" % (self.__class__.__name__, kwargs)

    def __str__(self) -> str:
        return repr(self)


class GremlinKubernetesAttackHelper(GremlinAttackHelper):
    '''
    k8s attacks require a completely different syntax on the API. All other logic is the same,
    so we just have to modify api_model.
    '''

    def api_model(self) -> dict:
        model: dict = {
            "targetDefinition": self._target.target_definition(),
            "impactDefinition": self._command.impact_definition()['commandArgs']
        }
        return model
