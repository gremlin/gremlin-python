# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging

from gremlinapi.cli import register_cli_action
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
    def list_users(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
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
        payload = cls._payload(**{'data': data})
        endpoint = '/users/auth'
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('auth_user_sso', ('',), ('',))
    def auth_user_sso(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        pass

    @classmethod
    @register_cli_action('invalidate_session', ('',), ('',))
    def invalidate_session(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        pass

    @classmethod
    @register_cli_action('email_companies', ('',), ('',))
    def email_companies(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        pass

    @classmethod
    @register_cli_action('saml_metadata', ('',), ('',))
    def saml_metadata(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        pass

class GremlinAPIUsersAuthMFA(GremlinAPI):
    def __init__(self):
        super.__init__(self)

    @classmethod
    @register_cli_action('auth_user_mfa', ('user', 'password', 'token', 'company',), ('get_company_session',))
    def auth_user(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        endpoint = '/users/auth/mfa/auth'
        payload = {
            'email': kwargs.get('user', None),
            'password': kwargs.get('password', None),
            'token': kwargs.get('mfa_token_value', None),
            'companyName': kwargs.get('company', None)
        }
        if not (payload['email'] and payload['password'] and payload['token'] and payload['companyName']):
            error_msg = f'User credential not supplied {kwargs}'
            log.fatal(error_msg)
            raise GremlinAuthError(error_msg)
        (resp, body) = https_client.api_call('POST', endpoint, **{'data': payload})
        return body