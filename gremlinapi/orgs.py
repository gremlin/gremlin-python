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


class GremlinAPIOrgs(GremlinAPI):
    @classmethod
    @register_cli_action("list_orgs", ("",), ("",))
    def list_orgs(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        endpoint: str = "/orgs"
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("get_org", ("identifier",), ("",))
    def get_org(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        identifier: str = cls._error_if_not_param("identifier", **kwargs)
        endpoint: str = f"/orgs/{identifier}"
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("create_org", ("name",), ("addUser",))
    def create_org(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        add_user: str = cls._info_if_not_param("addUser", True, **kwargs)
        endpoint: str = cls._add_query_param("/orgs", "addUser", add_user)
        data: dict = {"name": cls._error_if_not_param("name", **kwargs)}
        payload: dict = cls._payload(**{"headers": https_client.header(), "data": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("new_certificate", ("",), ("teamId",))
    def new_certificate(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        endpoint: str = cls._optional_team_endpoint("/orgs/auth/certificate", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("delete_certificate", ("",), ("teamId",))
    def delete_certificate(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "DELETE"
        endpoint: str = cls._optional_team_endpoint("/orgs/auth/certificate", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("delete_old_certificate", ("",), ("teamId",))
    def delete_old_certificate(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "DELETE"
        endpoint: str = cls._optional_team_endpoint(
            "/orgs/auth/certificate/old", **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("reset_secret", ("",), ("identifier", "teamId"))
    def reset_secret(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        endpoint: str = cls._optional_team_endpoint("/orgs/auth/secret/reset", **kwargs)
        data: dict = dict()
        identifier: str = cls._info_if_not_param("identifier", **kwargs)
        if identifier:
            data["identifier"] = identifier
        payload: dict = cls._payload(**{"headers": https_client.header(), "data": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body
