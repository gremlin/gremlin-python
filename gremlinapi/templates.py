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

from typing import Type, Union

from gremlinapi.gremlinapi import GremlinAPI
from gremlinapi.http_clients import (
    get_gremlin_httpclient,
    GremlinAPIurllibClient,
    GremlinAPIRequestsClient,
)


log = logging.getLogger("GremlinAPI.client")


class GremlinAPITemplates(GremlinAPI):
    @classmethod
    @register_cli_action("list_templates", ("",), ("teamId",))
    def list_templates(
        cls,
        https_client: Union[
            Type[GremlinAPIRequestsClient], Type[GremlinAPIurllibClient]
        ] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        endpoint: str = cls._optional_team_endpoint(f"/templates", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("create_template", ("body",), ("teamId",))
    def create_template(
        cls,
        https_client: Union[
            Type[GremlinAPIRequestsClient], Type[GremlinAPIurllibClient]
        ] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        data: dict = cls._error_if_not_json_body(**kwargs)
        endpoint: str = cls._optional_team_endpoint(f"/templates", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header(), "body": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("get_template", ("guid",), ("teamId",))
    def get_template(
        cls,
        https_client: Union[
            Type[GremlinAPIRequestsClient], Type[GremlinAPIurllibClient]
        ] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        guid: str = cls._error_if_not_param("guid", **kwargs)
        endpoint: str = cls._optional_team_endpoint(f"/templates/{guid}", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("delete_template", ("guid",), ("teamId",))
    def delete_template(
        cls,
        https_client: Union[
            Type[GremlinAPIRequestsClient], Type[GremlinAPIurllibClient]
        ] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "DELETE"
        guid: str = cls._error_if_not_param("guid", **kwargs)
        endpoint: str = cls._optional_team_endpoint(f"/templates/{guid}", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("list_command_templates", ("",), ("teamId",))
    def list_command_templates(
        cls,
        https_client: Union[
            Type[GremlinAPIRequestsClient], Type[GremlinAPIurllibClient]
        ] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        endpoint: str = cls._optional_team_endpoint(f"/templates/command", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("list_target_templates", ("",), ("teamId",))
    def list_target_templates(
        cls,
        https_client: Union[
            Type[GremlinAPIRequestsClient], Type[GremlinAPIurllibClient]
        ] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        endpoint: str = cls._optional_team_endpoint(f"/templates/target", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("list_trigger_templates", ("",), ("teamId",))
    def list_trigger_templates(
        cls,
        https_client: Union[
            Type[GremlinAPIRequestsClient], Type[GremlinAPIurllibClient]
        ] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        endpoint: str = cls._optional_team_endpoint(f"/templates/trigger", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body
