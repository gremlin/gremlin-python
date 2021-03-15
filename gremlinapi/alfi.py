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
from gremlinapi.http_clients import get_gremlin_httpclient,GremlinAPIRequestsClient,GremlinAPIurllibClient
from typing import Union

log = logging.getLogger("GremlinAPI.client")

class GremlinALFI(GremlinAPI):
    @classmethod
    @register_cli_action("create_alfi_experiment", ("body",), ("teamId"))
    def create_alfi_experiment(
        cls, https_client: Union[GremlinAPIRequestsClient,GremlinAPIurllibClient]=get_gremlin_httpclient(), *args, **kwargs
    ) -> str:
        method: str = "POST"
        data: str = cls._error_if_not_json_body(**kwargs)
        endpoint: str = cls._optional_team_endpoint("/experiments", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header(), "body": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("halt_all_alfi_experiments", ("",), ("teamId",))
    def halt_all_alfi_experiments(
        cls, https_client: Union[GremlinAPIRequestsClient,GremlinAPIurllibClient]=get_gremlin_httpclient(), *args, **kwargs
    ) -> str:
        method: str = "DELETE"
        endpoint: str = cls._optional_team_endpoint("/experiments", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("get_alfi_experiment_details", ("guid",), ("teamId",))
    def get_alfi_experiment_details(
        cls, https_client: Union[GremlinAPIRequestsClient,GremlinAPIurllibClient]=get_gremlin_httpclient(), *args, **kwargs
    ) -> str:
        method: str = "GET"
        guid: str = cls._error_if_not_param("guid", **kwargs)
        endpoint: str = cls._optional_team_endpoint(f"/experiments/{guid}", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("halt_alfi_experiment", ("guid",), ("teamId",))
    def halt_alfi_experiment(
        cls, https_client: Union[GremlinAPIRequestsClient,GremlinAPIurllibClient]=get_gremlin_httpclient(), *args, **kwargs
    ) -> str:
        method: str = "DELETE"
        guid: str = cls._error_if_not_param("guid", **kwargs)
        endpoint: str = cls._optional_team_endpoint(f"/experiments/{guid}", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("list_active_alfi_experiments", ("",), ("teamId",))
    def list_active_alfi_experiments(
        cls, https_client: Union[GremlinAPIRequestsClient,GremlinAPIurllibClient]=get_gremlin_httpclient(), *args, **kwargs
    ) -> str:
        method: str = "GET"
        endpoint: str = cls._optional_team_endpoint("/experiments/active", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("list_completed_alfi_experiments", ("",), ("teamId"))
    def list_completed_alfi_experiments(
        cls, https_client: Union[GremlinAPIRequestsClient,GremlinAPIurllibClient]=get_gremlin_httpclient(), *args, **kwargs
    ) -> str:
        method: str = "GET"
        endpoint: str = cls._optional_team_endpoint("/experiments/completed", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body
