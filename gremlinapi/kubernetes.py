# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging

from gremlinapi.cli import register_cli_action
from gremlinapi.exceptions import (
    GremlinParameterError,
    ProxyError,
    ClientError,
    HTTPTimeout,
    HTTPError,
)

from gremlinapi.gremlinapi import GremlinAPI
from gremlinapi.http_clients import (
    get_gremlin_httpclient,
    GremlinAPIHttpClient,
)

from typing import Union, Type

log = logging.getLogger("GremlinAPI.client")


class GremlinAPIKubernetesAttacks(GremlinAPI):
    @classmethod
    @register_cli_action("list_all_kubernetes_attacks", ("",), ("teamId",))
    def list_all_kubernetes_attacks(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        endpoint: str = cls._optional_team_endpoint("/kubernetes/attacks", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("get_kubernetes_attack", ("uid",), ("teamId",))
    def get_kubernetes_attack(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        uid: str = cls._error_if_not_param("uid", **kwargs)
        endpoint: str = cls._optional_team_endpoint(
            f"/kubernetes/attacks/{uid}", **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("halt_kubernetes_attack", ("uid",), ("teamId",))
    def halt_kubernetes_attack(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        uid: str = cls._error_if_not_param("uid", **kwargs)
        endpoint: str = cls._optional_team_endpoint(
            f"/kubernetes/attacks/{uid}/halt", **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("halt_all_kubernetes_attacks", ("",), ("teamId",))
    def halt_all_kubernetes_attacks(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        endpoint: str = cls._optional_team_endpoint(
            "/kubernetes/attacks/halt", **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("new_kubernetes_attack", ("body",), ("teamId",))
    def new_kubernetes_attack(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        data: dict = cls._error_if_not_json_body(**kwargs)
        endpoint: str = cls._optional_team_endpoint("/kubernetes/attacks/new", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header(), "body": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body


class GremlinAPIKubernetesTargets(GremlinAPI):
    @classmethod
    @register_cli_action("list_kubernetes_targets", ("",), ("teamId",))
    def list_kubernetes_targets(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        endpoint: str = cls._optional_team_endpoint("/kubernetes/targets", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body
