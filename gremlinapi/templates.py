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
    GremlinAPIHttpClient,
)


log = logging.getLogger("GremlinAPI.client")


class GremlinAPITemplates(GremlinAPI):
    @classmethod
    @register_cli_action("list_templates", ("",), ("teamId",))
    def list_templates(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        error_message: str = f"This function is now deprecated, please refactor around"
        log.error(error_message)
        raise NotImplementedError(error_message)

    @classmethod
    @register_cli_action("create_template", ("body",), ("teamId",))
    def create_template(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        error_message: str = f"This function is now deprecated, please refactor around"
        log.error(error_message)
        raise NotImplementedError(error_message)

    @classmethod
    @register_cli_action("get_template", ("guid",), ("teamId",))
    def get_template(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        error_message: str = f"This function is now deprecated, please refactor around"
        log.error(error_message)
        raise NotImplementedError(error_message)

    @classmethod
    @register_cli_action("delete_template", ("guid",), ("teamId",))
    def delete_template(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        error_message: str = f"This function is now deprecated, please refactor around"
        log.error(error_message)
        raise NotImplementedError(error_message)

    @classmethod
    @register_cli_action("list_command_templates", ("",), ("teamId",))
    def list_command_templates(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        error_message: str = f"This function is now deprecated, please refactor around"
        log.error(error_message)
        raise NotImplementedError(error_message)

    @classmethod
    @register_cli_action("list_target_templates", ("",), ("teamId",))
    def list_target_templates(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        error_message: str = f"This function is now deprecated, please refactor around"
        log.error(error_message)
        raise NotImplementedError(error_message)

    @classmethod
    @register_cli_action("list_trigger_templates", ("",), ("teamId",))
    def list_trigger_templates(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        error_message: str = f"This function is now deprecated, please refactor around"
        log.error(error_message)
        raise NotImplementedError(error_message)
