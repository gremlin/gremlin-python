# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging

from gremlinapi.cli import register_cli_action

from gremlinapi.exceptions import GremlinAuthError

from gremlinapi.http_clients import get_gremlin_httpclient
from gremlinapi.config import GremlinAPIConfig

log = logging.getLogger('GremlinAPI.client')


class GremlinAPIUsers(object):

    def __init__(self):
        pass

    @classmethod
    @register_cli_action('list_user', ('',), ('teamId',))
    def list_users(cls, https_client=get_gremlin_httpclient(), **kwargs):
        endpoint = '/users'
        payload = {'teamId': kwargs.get('teamId', None)}
        if not (payload['teamId']):
            error_msg = f'Missing teamId from request, assuming non-RBAC enabled request'
            log.debug(error_msg)
        else:
            endpoint += f'?teamId={payload["teamId"]}'
        headers = https_client.header()
        (resp, body) = https_client.api_call('GET', endpoint, **{'headers':headers})
        return body

    @classmethod
    @register_cli_action('invite_user', ('',), ('',))
    def invite_user(cls, https_client=get_gremlin_httpclient(), **kwargs):
        endpoint = '/users/invite'
        pass

    @classmethod
    @register_cli_action('delete_user', ('email',), ('',))
    def delete_user(cls, https_client=get_gremlin_httpclient(), **kwargs):
        enpoint = '/users'
        pass

    @classmethod
    @register_cli_action('update_user', ('',), ('',))
    def update_user(cls, https_client=get_gremlin_httpclient(), **kwargs):
        enpoint = '/users'
        pass

class GremlinAPIUsersAuth(object):

    def __init__(self):
        pass

    @classmethod
    @register_cli_action('auth_user', ('',), ('',))
    def auth_user(cls, https_client=get_gremlin_httpclient(), **kwargs):
        endpoint = '/users/auth'
        payload = {
            'email': kwargs.get('user', None),
            'password': kwargs.get('password', None),
            'companyName': kwargs.get('company', None)
        }
        if not (payload['email'] and payload['password'] and payload['companyName']):
            error_msg = f'User credential not supplied {kwargs}'
            log.fatal(error_msg)
            raise GremlinAuthError(error_msg)
        (resp, body) = https_client.api_call('POST', endpoint, **{'data': payload})
        return body

    @classmethod
    @register_cli_action('auth_user_sso', ('',), ('',))
    def auth_user_sso(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    @register_cli_action('invalidate_session', ('',), ('',))
    def invalidate_session(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    @register_cli_action('email_companies', ('',), ('',))
    def email_companies(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    @register_cli_action('saml_metadata', ('',), ('',))
    def saml_metadata(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

class GremlinAPIUsersAuthMFA(object):
    @classmethod
    @register_cli_action('auth_user_mfa', ('user', 'password', 'token', 'company',), ('get_company_session',))
    def auth_user(cls, https_client=get_gremlin_httpclient(), **kwargs):
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