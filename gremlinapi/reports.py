# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging

from datetime import date

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


class GremlinAPIReports(GremlinAPI):
    @classmethod
    @register_cli_action("report_attacks", ("",), ("start", "end", "period", "teamId"))
    def report_attacks(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        params: list = ["start", "end", "period"]
        endpoint: str = cls._build_query_string_option_team_endpoint(
            "/reports/attacks", params, **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("report_clients", ("",), ("start", "end", "period", "teamId"))
    def report_clients(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        params: list = ["start", "end", "period"]
        endpoint: str = cls._build_query_string_option_team_endpoint(
            "/reports/clients", params, **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action(
        "report_companies", ("",), ("start", "end", "period", "teamId")
    )
    def report_companies(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        params: list = ["startDate", "endDate"]
        endpoint: str = cls._build_query_string_endpoint(
            "/reports/companies", params, **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    def report_pricing(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        params: list = ["startDate", "endDate", "trackingPeriod"]
        endpoint: str = cls._build_query_string_endpoint(
            "/reports/pricing", params, **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("report_teams", ("",), ("start", "end", "period", "teamId"))
    def report_teams(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        params: list = ["startDate", "endDate"]
        endpoint: str = cls._build_query_string_option_team_endpoint(
            "/reports/teams", params, **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("report_users", ("",), ("start", "end", "period", "teamId"))
    def report_users(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        params: list = ["start", "end", "period"]
        endpoint: str = cls._build_query_string_option_team_endpoint(
            "/reports/users", params, **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body


class GremlinAPIReportsSecurity(GremlinAPI):
    @classmethod
    @register_cli_action("report_security_access", ("start", "end"), ("",))
    def report_security_access(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        params: list = ["start", "end"]
        endpoint: str = cls._build_query_string_endpoint(
            "/reports/security/access", params, **kwargs
        )
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body
