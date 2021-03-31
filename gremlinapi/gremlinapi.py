# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import json
import logging
import time

from gremlinapi.config import GremlinAPIConfig as config

from gremlinapi.exceptions import (
    APIError,
    GremlinParameterError,
    ProxyError,
    ClientError,
    HTTPTimeout,
    HTTPError,
)

from typing import Optional, Dict, Any

from gremlinapi.http_clients import get_gremlin_httpclient
from gremlinapi.exceptions import GremlinParameterError

log = logging.getLogger("GremlinAPI.client")


class GremlinAPI(object):
    def __init__(self):
        pass

    @classmethod
    def _add_query_param(cls, endpoint: str, param_name: str, param_value: str) -> str:
        if endpoint and param_name and param_value:
            if "/?" in endpoint and not (
                str(endpoint).endswith("?") or str(endpoint).endswith("&")
            ):
                endpoint += f"&{param_name}={param_value}"
            elif "/?" in endpoint and (
                str(endpoint).endswith("?") or str(endpoint).endswith("&")
            ):
                endpoint += f"{param_name}={param_value}"
            elif "/?" not in endpoint:
                endpoint += f"/?{param_name}={param_value}"
        return endpoint

    @classmethod
    def _build_query_string_endpoint(
        cls, endpoint: str, params: list, **kwargs: dict
    ) -> str:
        if not endpoint:
            error_msg: str = "expected endpoint, received nothing"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        if not params or type(params) != type(list()):
            error_msg = f"Expected list of params, received {type(params)}"
            log.error(error_msg)
            raise (GremlinParameterError(error_msg))
        for param_name in params:
            # maps pythonic param_name to API paramName
            if param_name is "team_id":
                endpoint = cls._add_query_param(
                    endpoint, "teamId", cls._error_if_not_param(param_name, **kwargs)
                )
            else:
                endpoint = cls._add_query_param(
                    endpoint, param_name, cls._error_if_not_param(param_name, **kwargs)
                )
        return endpoint

    @classmethod
    def _build_query_string_option_team_endpoint(
        cls, endpoint: str, params: list, **kwargs: dict
    ) -> str:
        endpoint = cls._build_query_string_endpoint(endpoint, params, **kwargs)
        if "team_id" not in params:
            endpoint = cls._optional_team_endpoint(endpoint, **kwargs)
        return endpoint

    @classmethod
    def _build_query_string_required_team_endpoint(
        cls, endpoint: str, params: list, **kwargs: dict
    ) -> str:
        endpoint = cls._build_query_string_endpoint(endpoint, params, **kwargs)
        if "team_id" not in params:
            endpoint = cls._required_team_endpoint(endpoint, **kwargs)
        return endpoint

    @classmethod
    def _optional_team_endpoint(cls, endpoint: str, **kwargs: dict) -> str:
        team_id: str = cls._info_if_not_param("team_id", **kwargs)
        if not team_id and type(config.team_id) is str:
            team_id = config.team_id  # type: ignore
        if team_id:
            endpoint = cls._add_query_param(endpoint, "teamId", team_id)
        return endpoint

    @classmethod
    def _required_team_endpoint(cls, endpoint: str, **kwargs: dict) -> str:
        team_id: str = cls._warn_if_not_param("team_id", **kwargs)
        if not team_id and type(config.team_id) is str:
            team_id = config.team_id  # type: ignore
        else:
            error_msg: str = f"Endpoint requires a team_id, none supplied"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        endpoint = cls._add_query_param(endpoint, "teamId", team_id)
        return endpoint

    @classmethod
    def _error_if_not_json_body(cls, **kwargs: dict) -> dict:
        body: dict = cls._warn_if_not_json_body(**kwargs)
        if not body:
            error_msg: str = f"JSON Body not supplied: {kwargs}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        return body

    @classmethod
    def _error_if_not_email(cls, **kwargs: dict) -> str:
        email: str = cls._info_if_not_param("email", **kwargs)
        if not email:
            error_msg: str = f"email address not passed: {kwargs}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        # Do some email regex validation here...
        return email

    @classmethod
    def _error_if_not_param(cls, parameter_name: str, **kwargs: dict) -> str:
        param: str = cls._info_if_not_param(parameter_name, **kwargs)
        if not param:
            error_msg: str = f"{parameter_name} not supplied: {kwargs}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        return param

    @classmethod
    def _info_if_not_param(cls, parameter_name: str, default="", **kwargs: dict) -> str:
        param: str = kwargs.get(parameter_name, "")  # type: ignore
        if not param:
            error_msg: str = f"{parameter_name} not found in arguments: {kwargs}"
            log.info(error_msg)
            param = default
        return param

    @classmethod
    def _payload(cls, **kwargs: dict) -> dict:
        headers = kwargs.get("headers", None)  # type: ignore
        body = kwargs.get("body", None)  # type: ignore
        data = kwargs.get("data", None)  # type: ignore
        payload: dict = {"headers": headers, "data": data, "body": body}
        payload = {k: v for k, v in payload.items() if v is not None}
        return payload

    @classmethod
    def _warn_if_not_json_body(cls, **kwargs: dict) -> dict:
        body: dict = cls._info_if_not_param("body", **kwargs)  # type: ignore
        if not body:
            error_msg: str = f"JSON Body not supplied: {kwargs}"
            log.warning(error_msg)
        # Do some json validation
        return body

    @classmethod
    def _warn_if_not_param(
        cls, parameter_name: str, default=None, **kwargs: dict
    ) -> str:
        param: str = cls._info_if_not_param(parameter_name, **kwargs)  # type: ignore
        if not param:
            error_msg: str = f"{parameter_name} not found in arguments: {kwargs}"
            log.warning(error_msg)
            param = default
        return param
