# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging

from gremlinapi.cli import register_cli_action
from gremlinapi.config import GremlinAPIConfig
from gremlinapi.exceptions import (
    GremlinParameterError,
    GremlinAuthError,
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

from typing import Type, Union


log = logging.getLogger("GremlinAPI.client")


class GremlinAPIUsers(GremlinAPI):
    @classmethod
    def _error_if_not_valid_role_statement(cls, **kwargs) -> str:
        role: str = kwargs.get("role", "")
        if not role:
            error_msg: str = f"Role object not passed to users endpoint: {kwargs}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        return role

    @classmethod
    @register_cli_action("list_user", ("",), ("teamId",))
    def list_users(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        endpoint: str = cls._optional_team_endpoint(f"/users", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("add_user_to_team", ("body",), ("teamId",))
    def add_user_to_team(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        data: Union[list, dict] = cls._error_if_not_json_body(**kwargs)
        if isinstance(data, dict):
            data = [dict(data)]
        endpoint: str = cls._optional_team_endpoint(f"/users", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header(), "body": data})  # type: ignore
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("update_user", ("email", "role"), ("teamId",))
    def update_user(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "PUT"
        email: str = cls._error_if_not_email(**kwargs)
        role: str = cls._error_if_not_valid_role_statement(**kwargs)
        endpoint: str = cls._optional_team_endpoint(f"/users/{email}", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header(), "data": role})  # type: ignore
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("deactivate_user", ("email",), ("teamId",))
    def deactivate_user(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "DELETE"
        email: str = cls._error_if_not_email(**kwargs)
        endpoint: str = cls._optional_team_endpoint(f"/users/{email}", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("list_active_user", ("",), ("teamId",))
    def list_active_users(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        endpoint: str = cls._optional_team_endpoint(f"/users/active", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("invite_user", ("email",), ("teamId",))
    def invite_user(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        email: str = cls._error_if_not_email(**kwargs)
        endpoint: str = cls._optional_team_endpoint(f"/users/invite", **kwargs)
        data: dict = {"email": email}
        payload: dict = cls._payload(**{"headers": https_client.header(), "data": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("revoke_user_invite", ("email",), ("teamId",))
    def revoke_user_invite(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "DELETE"
        email: str = cls._error_if_not_email(**kwargs)
        endpoint: str = cls._optional_team_endpoint(f"/users/invite/{email}", **kwargs)
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action(
        "renew_user_authorization", ("email", "orgId", "renewToken"), ("",)
    )
    def renew_user_authorization(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        email: str = cls._error_if_not_email(**kwargs)
        org_id: str = kwargs.get("orgId", None)  # type: ignore
        renew_token: str = kwargs.get("renewToken", None)  # type: ignore
        if not org_id:
            error_msg: str = f"orgId required parameter not supplied: {kwargs}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        if not renew_token:
            error_msg = f"renewToken required parameter not supplied: {kwargs}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        data: dict = {"email": email, "orgId": org_id, "renewToken": renew_token}
        endpoint: str = f"/users/renew"
        payload: dict = cls._payload(**{"headers": https_client.header(), "data": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action(
        "renew_user_authorization_rbac",
        ("email", "companyId", "teamId", "renewToken"),
        ("",),
    )
    def renew_user_authorization_rbac(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        email: str = cls._error_if_not_email(**kwargs)
        company_id: str = kwargs.get("companyId", None)  # type: ignore
        team_id: str = cls._error_if_not_param("teamId", **kwargs)
        renew_token: str = kwargs.get("renewToken", None)  # type: ignore
        if not company_id:
            error_msg: str = f"orgId required parameter not supplied: {kwargs}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        if not renew_token:
            error_msg = f"renewToken required parameter not supplied: {kwargs}"
            log.error(error_msg)
            raise GremlinParameterError(error_msg)
        data: dict = {
            "email": email,
            "companyId": company_id,
            "teamId": team_id,
            "renewToken": renew_token,
        }
        endpoint: str = f"/users/renew/rbac"
        payload: dict = cls._payload(**{"headers": https_client.header(), "data": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("get_user_self", ("",), ("",))
    def get_user_self(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        endpoint: str = f"/users/self"
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("update_user_self", ("body",), ("",))
    def update_user_self(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "PATCH"
        data: dict = cls._error_if_not_json_body(**kwargs)
        endpoint: str = f"/users/self"
        payload: dict = cls._payload(**{"headers": https_client.header(), "body": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("get_user_session", ("",), ("getCompanySession",))
    def get_user_session(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        get_company_session: str = kwargs.get("getCompanySession", None)  # type: ignore
        endpoint: str = f"/users/sessions"
        if get_company_session:
            endpoint += f"/?getCompanySession=true"
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body


class GremlinAPIUsersAuth(GremlinAPI):
    @classmethod
    @register_cli_action(
        "auth_user",
        (
            "email",
            "password",
            "companyName",
        ),
        ("getCompanySession",),
    )
    def auth_user(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        data: dict = {
            "email": cls._error_if_not_param("email", **kwargs),
            "password": cls._error_if_not_param("password", **kwargs),
            "companyName": cls._error_if_not_param("companyName", **kwargs),
        }
        get_company_session: str = cls._info_if_not_param("getCompanySession", **kwargs)
        payload: dict = cls._payload(**{"data": data})
        endpoint: str = "/users/auth"
        if get_company_session:
            endpoint += "/?getCompanySession=true"
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action(
        "auth_user_sso",
        ("accessToken", "email", "provider", "companyName"),
        ("getCompanySession",),
    )
    def auth_user_sso(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        data: dict = {
            "accessToken": cls._error_if_not_param("accessToken", **kwargs),
            "email": cls._error_if_not_param("email", **kwargs),
            "provider": cls._error_if_not_param("provider", **kwargs),
            "companyName": cls._error_if_not_param("companyName", **kwargs),
        }
        get_company_session: str = cls._info_if_not_param("getCompanySession", **kwargs)
        payload: dict = cls._payload(**{"data": data})
        endpoint: str = "/users/auth"
        if get_company_session:
            endpoint += "/?getCompanySession=true"
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("invalidate_session", ("",), ("",))
    def invalidate_session(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "DELETE"
        endpoint: str = "/users/auth"
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("get_company_affiliations", ("email",), ("",))
    def get_company_affiliations(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        email: str = cls._error_if_not_email(**kwargs)
        endpoint: str = f"/users/auth/emailCompanies/?email={email}"
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("get_saml_metadata", ("",), ("",))
    def get_saml_metadata(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        endpoint: str = "/users/auth/saml/metadata"
        (resp, body) = https_client.api_call(method, endpoint)
        return body


class GremlinAPIUsersAuthMFA(GremlinAPI):
    @classmethod
    @register_cli_action(
        "auth_user_mfa",
        (
            "email",
            "password",
            "token",
            "company",
        ),
        ("getCompanySession",),
    )
    def auth_user(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        data: dict = {
            "email": kwargs.get("email", None),
            "password": kwargs.get("password", None),
            "token": kwargs.get("token", None),
            "companyName": kwargs.get("company", None),
        }
        get_company_session: str = cls._info_if_not_param("getCompanySession", **kwargs)
        payload: dict = cls._payload(**{"data": data})
        endpoint: str = "/users/auth/mfa/auth"
        if get_company_session:
            endpoint += "/?getCompanySession=true"
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    def auth_user_mfa(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        # Alias to auth_user
        return cls.auth_user(https_client, *args, **kwargs)

    @classmethod
    @register_cli_action("get_mfa_status", ("email",), ("",))
    def get_mfa_status(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        email: str = cls._error_if_not_email(**kwargs)
        endpoint: str = f"/users/auth/mfa/{email}/enabled"
        (resp, body) = https_client.api_call(method, endpoint)
        return body

    @classmethod
    @register_cli_action("get_user_mfa_status", ("",), ("",))
    def get_user_mfa_status(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "GET"
        endpoint: str = "/users/auth/mfa/info"
        payload: dict = cls._payload(**{"headers": https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action(
        "disable_mfa",
        (
            "email",
            "password",
            "token",
        ),
        ("",),
    )
    def disable_mfa(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        data: dict = {
            "email": cls._error_if_not_email(**kwargs),
            "password": cls._error_if_not_param("password", **kwargs),
            "token": cls._error_if_not_param("token", **kwargs),
        }
        endpoint: str = "/users/auth/mfa/disable"
        payload: dict = cls._payload(**{"data": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action("force_disable_mfa", ("email",), ("",))
    def force_disable_mfa(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        data: dict = {"email": cls._error_if_not_email(**kwargs)}
        endpoint: str = "/users/auth/mfa/forceDisable"
        payload: dict = cls._payload(**{"headers": https_client.header(), "data": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action(
        "enable_mfa",
        (
            "email",
            "password",
            "provider",
        ),
        ("",),
    )
    def enable_mfa(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        data: dict = {
            "email": cls._error_if_not_email(**kwargs),
            "password": cls._error_if_not_param("password", **kwargs),
            "provider": cls._error_if_not_param("provider", **kwargs),
        }
        endpoint: str = "/users/auth/mfa/enable"
        payload: dict = cls._payload(**{"data": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action(
        "validate_token",
        (
            "email",
            "token",
        ),
        ("",),
    )
    def validate_token(
        cls,
        https_client: Type[GremlinAPIHttpClient] = get_gremlin_httpclient(),
        *args: tuple,
        **kwargs: dict,
    ) -> dict:
        method: str = "POST"
        data: dict = {
            "email": cls._error_if_not_email(**kwargs),
            "token": cls._error_if_not_param("token", **kwargs),
        }
        endpoint: str = "/users/auth/mfa/validate"
        payload: dict = cls._payload(**{"data": data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body
