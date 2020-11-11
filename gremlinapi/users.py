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
    HTTPError
)

from gremlinapi.gremlinapi import GremlinAPI
from gremlinapi.http_clients import get_gremlin_httpclient


log = logging.getLogger('GremlinAPI.client')


class GremlinAPIUsers(GremlinAPI):

    @classmethod
    def _error_if_not_valid_role_statement(cls, **kwargs):
        role = kwargs.get('role', None)
        if not role:
            error_msg = f'Role object not passed to users endpoint: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        return role

    @classmethod
    @register_cli_action('list_user', ('',), ('teamId',))
    def list_users(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._optional_team_endpoint(f'/users', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('add_user_to_team', ('body',), ('teamId',))
    def add_user_to_team(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        data = cls._error_if_not_json_body(**kwargs)
        if isinstance(data, dict):
            data = [dict(data)]
        endpoint = cls._optional_team_endpoint(f'/users', **kwargs)
        payload = cls._payload(**{'headers': https_client.header(), 'body': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('update_user', ('email', 'role'), ('teamId',))
    def update_user(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'PUT'
        email = cls._error_if_not_email(**kwargs)
        role = cls._error_if_not_valid_role_statement(**kwargs)
        endpoint = cls._optional_team_endpoint(f'/users/{email}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header(), 'data': role})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('deactivate_user', ('email',), ('teamId',))
    def deactivate_user(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'DELETE'
        email = cls._error_if_not_email(**kwargs)
        endpoint = cls._optional_team_endpoint(f'/users/{email}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('list_active_user', ('',), ('teamId',))
    def list_active_users(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._optional_team_endpoint(f'/users/active', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('invite_user', ('email',), ('teamId',))
    def invite_user(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        email = cls._error_if_not_email(**kwargs)
        endpoint = cls._optional_team_endpoint(f'/users/invite', **kwargs)
        data = {'email': email}
        payload = cls._payload(**{'headers': https_client.header(), 'data': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('revoke_user_invite', ('email',), ('teamId',))
    def revoke_user_invite(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'DELETE'
        email = cls._error_if_not_email(**kwargs)
        endpoint = cls._optional_team_endpoint(f'/users/invite/{email}', **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('renew_user_authorization', ('email', 'orgId', 'renewToken'), ('',))
    def renew_user_authorization(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        email = cls._error_if_not_email(**kwargs)
        org_id = kwargs.get('orgId', None)
        renew_token = kwargs.get('renewToken', None)
        if not org_id:
            error_msg = f'orgId required parameter not supplied: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        if not renew_token:
            error_msg = f'renewToken required parameter not supplied: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        data = {'email': email, 'orgId': org_id, 'renewToken': renew_token}
        endpoint = f'/users/renew'
        payload = cls._payload(**{'headers': https_client.header(), 'data': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('renew_user_authorization_rbac', ('email', 'companyId', 'teamId', 'renewToken'), ('',))
    def renew_user_authorization_rbac(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        email = cls._error_if_not_email(**kwargs)
        company_id = kwargs.get('companyId', None)
        team_id =  cls._error_if_not_param('teamnId', **kwargs)
        renew_token = kwargs.get('renewToken', None)
        if not company_id:
            error_msg = f'orgId required parameter not supplied: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        if not renew_token:
            error_msg = f'renewToken required parameter not supplied: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        data = {'email': email, 'companyId': company_id, 'teamId': team_id, 'renewToken': renew_token}
        endpoint = f'/users/renew/rbac'
        payload = cls._payload(**{'headers': https_client.header(), 'data': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('get_user_self', ('',), ('',))
    def get_user_self(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = f'/users/self'
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('update_user_self', ('body',), ('',))
    def get_user_self(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'PATCH'
        data = cls._error_if_not_json_body(**kwargs)
        endpoint = f'/users/self'
        payload = cls._payload(**{'headers': https_client.header(), 'body': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('get_user_session', ('',), ('getCompanySession',))
    def get_user_session(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        get_company_session = kwargs.get('getCompanySession', None)
        endpoint = f'/users/sessions'
        if get_company_session:
            endpoint += f'/?getCompanySession=true'
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body


class GremlinAPIUsersAuth(GremlinAPI):

    @classmethod
    @register_cli_action('auth_user', ('email', 'password', 'companyName',), ('getCompanySession',))
    def auth_user(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        data = {
            'email': cls._error_if_not_param('email', **kwargs),
            'password': cls._error_if_not_param('password', **kwargs),
            'companyName': cls._error_if_not_param('companyName', **kwargs)
        }
        get_company_session = cls._info_if_not_param('getCompanySession', **kwargs)
        payload = cls._payload(**{'data': data})
        endpoint = '/users/auth'
        if get_company_session:
            endpoint += '/?getCompanySession=true'
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('auth_user_sso', ('accessToken', 'email', 'provider', 'companyName'), ('getCompanySession',))
    def auth_user_sso(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        data = {
            'accessToken': cls._error_if_not_param('accessToken', **kwargs),
            'email': cls._error_if_not_param('email', **kwargs),
            'provider': cls._error_if_not_param('provider', **kwargs),
            'companyName': cls._error_if_not_param('companyName', **kwargs)
        }
        get_company_session = cls._info_if_not_param('getCompanySession', **kwargs)
        payload = cls._payload(**{'data': data})
        endpoint = '/users/auth'
        if get_company_session:
            endpoint += '/?getCompanySession=true'
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('invalidate_session', ('',), ('',))
    def invalidate_session(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'DELETE'
        endpoint = '/users/auth'
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('get_company_affiliations', ('email',), ('',))
    def get_company_affiliations(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        email = cls._error_if_not_email(**kwargs)
        endpoint = f'/users/auth/emailCompanies/?email={email}'
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('get_saml_metadata', ('',), ('',))
    def get_saml_metadata(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = '/users/auth/saml/metadata'
        (resp, body) = https_client.api_call(method, endpoint)
        return body

class GremlinAPIUsersAuthMFA(GremlinAPI):

    @classmethod
    @register_cli_action('auth_user_mfa', ('email', 'password', 'token', 'company',), ('getCompanySession',))
    def auth_user(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        data = {
            'email': kwargs.get('email', None),
            'password': kwargs.get('password', None),
            'token': kwargs.get('token', None),
            'companyName': kwargs.get('company', None)
        }
        get_company_session = cls._info_if_not_param('getCompanySession', **kwargs)
        payload = cls._payload(**{'data': data})
        endpoint = '/users/auth/mfa/auth'
        if get_company_session:
            endpoint += '/?getCompanySession=true'
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    def auth_user_mfa(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        # Alias to auth_user
        return cls.auth_user(https_client, *args, **kwargs)

    @classmethod
    @register_cli_action('get_mfa_status', ('email',), (''))
    def get_mfa_status(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        email = cls._error_if_not_email(**kwargs)
        endpoint = f'/users/auth/mfa/{email}/enabled'
        (resp, body) = https_client.api_call(method, endpoint)
        return body

    @classmethod
    @register_cli_action('get_user_mfa_status', ('',), ('',))
    def get_user_mfa_status(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = '/users/auth/mfa/info'
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('disable_mfa', ('email', 'password', 'token',), ('',))
    def disable_mfa(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        data = {
            'email': cls._error_if_not_email(**kwargs),
            'password': cls._error_if_not_param('password', **kwargs),
            'token': cls._error_if_not_param('token', **kwargs)
        }
        endpoint = '/users/auth/mfa/disable'
        payload = cls._payload(**{'data': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('force_disable_mfa', ('email',), ('',))
    def force_disable_mfa(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        data = {
            'email': cls._error_if_not_email(**kwargs)
        }
        endpoint = '/users/auth/mfa/forceDisable'
        payload = cls._payload(**{'headers': https_client.header(), 'data': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('enable_mfa', ('email', 'password', 'provider',), ('',))
    def enable_mfa(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        data = {
            'email': cls._error_if_not_email(**kwargs),
            'password': cls._error_if_not_param('password', **kwargs),
            'provider': cls._error_if_not_param('provider', **kwargs)
        }
        endpoint = '/users/auth/mfa/enable'
        payload = cls._payload(**{'data': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('validate_token', ('email', 'token',), (''))
    def validate_token(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        data = {
            'email': cls._error_if_not_email(**kwargs),
            'token': cls._error_if_not_param('token', **kwargs)
        }
        endpoint = '/users/auth/mfa/validate'
        payload = cls._payload(**{'data': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

