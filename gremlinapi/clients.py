# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging

from typing import Union, Type, Any

from gremlinapi.cli import register_cli_action
from gremlinapi.exceptions import (
    GremlinParameterError,
    ProxyError,
    ClientError,
    HTTPTimeout,
    HTTPError,
)
from gremlinapi.http_clients import GremlinAPIHttpClient
from gremlinapi.config import GremlinAPIConfig
from gremlinapi.gremlinapi import GremlinAPI
from gremlinapi.http_clients import get_gremlin_httpclient

log = logging.getLogger("GremlinAPI.client")


class GremlinAPIClients(GremlinAPI):
    @classmethod
    @register_cli_action("activate_client", ("guid",), ("teamId",))
    def activate_client(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        **kwargs: dict,
    ) -> dict:
        method: str = "PUT"
        guid: str = cls._error_if_not_param("guid", **kwargs)
        endpoint: str = cls._optional_team_endpoint(
            f"/clients/{guid}/activate", **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("deactivate_client", ("guid",), ("teamId",))
    def deactivate_client(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        **kwargs: dict,
    ) -> dict:
        method: str = "DELETE"
        guid: str = cls._error_if_not_param("guid", **kwargs)
        endpoint: str = cls._optional_team_endpoint(f"/clients/{guid}", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("list_active_clients", ("",), ("teamId",))
    def list_active_clients(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        endpoint: str = cls._optional_team_endpoint(f"/clients/active", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("list_clients", ("",), ("teamId",))
    def list_clients(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        endpoint: str = cls._optional_team_endpoint(f"/clients", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    def get_update_client_target_cache(cls) -> [dict]:
        if (not GremlinAPIConfig.client_cache) or (type(GremlinAPIConfig.client_cache) == type(property())):
            GremlinAPIConfig.client_cache = GremlinAPIClients.list_clients()
        # Collects all containers
        total_containers = []
        active_clients = GremlinAPIConfig.client_cache['active']
        for ac in active_clients:
            for container in ac['containers']:
                total_containers.append(container)
        inactive_clients = GremlinAPIConfig.client_cache['inactive']
        for iac in inactive_clients:
            for container in iac['containers']:
                total_containers.append(container)
        idle_clients = GremlinAPIConfig.client_cache['idle']
        for ic in idle_clients:
            for container in ic['containers']:
                total_containers.append(container)
        return total_containers
