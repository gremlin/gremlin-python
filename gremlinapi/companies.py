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
    HTTPError
)

from gremlinapi.gremlinapi import GremlinAPI
from gremlinapi.http_clients import get_gremlin_httpclient


log = logging.getLogger('GremlinAPI.client')


class GremlinAPICompanies(GremlinAPI):

    @classmethod
    def _error_if_not_email(cls, **kwargs):
        email = kwargs.get('email', None)
        if not email:
            error_msg = f'No email address provided: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        return email

    @classmethod
    @register_cli_action('get_company', ('identifier',), ('',))
    def get_company(cls, https_client=get_gremlin_httpclient(), **kwargs):
        identifier = cls._error_if_not_identifier(**kwargs)
        endpoint = f'/companies/{identifier}'
        method = 'GET'
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

    @classmethod
    @register_cli_action('list_company_clients', ('identifier',), ('',))
    def list_company_clients(cls, https_client=get_gremlin_httpclient(), **kwargs):
        identifier = cls._error_if_not_identifier(**kwargs)
        endpoint = f'/companies/{identifier}/clients'
        method = 'GET'
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

    @classmethod
    @register_cli_action('invite_company_user', ('identifier', 'body'), ('',))
    def invite_company_user(cls, https_client=get_gremlin_httpclient(), **kwargs):
        identifier = cls._error_if_not_identifier(**kwargs)
        data = cls._error_if_not_body(**kwargs)
        endpoint = f'/companies/{identifier}/invites'
        method = 'POST'
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'body': data, 'headers': headers})
        return body

    @classmethod
    @register_cli_action('delete_company_invite', ('identifier', 'email'), ('',))
    def delete_company_invite(cls, https_client=get_gremlin_httpclient(), **kwargs):
        identifier = cls._error_if_not_identifier(**kwargs)
        email = cls._error_if_not_email(**kwargs)
        endpoint = f'/companies/{identifier}/invites/{email}'
        method = 'DELETE'
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

    @classmethod
    @register_cli_action('company_mfa_prefs', ('identifier',), ('forceMfa', 'mfaProviders', 'defaultMfaProvider',))
    def company_mfa_prefs(cls, https_client=get_gremlin_httpclient(), **kwargs):
        identifier = cls._error_if_not_identifier(**kwargs)
        endpoint = f'/companies/{identifier}/mfaPrefs'
        method = 'POST'
        headers = https_client.header()
        data = {
            'forceMfa': kwargs.get('forceMfa', None),
            'mfaProviders': kwargs.get('mfaProviders', None),
            'defaultMfaProvider': kwargs.get('defaultMfaProvider', None)
        }
        data = {k: v for k, v in data.items() if v is not None}
        (resp, body) = https_client.api_call(method, endpoint, **{'data': data, 'headers': headers})
        return body

    @classmethod
    @register_cli_action('update_company_prefs', ('identifier',), ('domain',))
    def update_company_prefs(cls, https_client=get_gremlin_httpclient(), **kwargs):
        identifier = cls._error_if_not_identifier(**kwargs)
        endpoint = f'/companies/{identifier}/prefs'
        method = 'POST'
        headers = https_client.header()
        data = {'domain': kwargs.get('domain', None)}
        data = {k: v for k, v in data.items() if v is not None}
        (resp, body) = https_client.api_call(method, endpoint, **{'data': data, 'headers': headers})
        return body

    @classmethod
    @register_cli_action('update_company_saml_props',
                         ('identifier',),
                         ('enabled', 'entityId', 'idpUrl', 'certificate', 'forced'))
    def update_company_saml_props(cls, https_client=get_gremlin_httpclient(), **kwargs):
        identifier = cls._error_if_not_identifier(**kwargs)
        endpoint = f'/companies/{identifier}/saml/props'
        method = 'POST'
        headers = https_client.header()
        data = {
            'enabled': kwargs.get('enabled', None),
            'entityId': kwargs.get('entityId', None),
            'idpUrl': kwargs.get('idpUrl', None),
            'certificate': kwargs.get('certificate', None),
            'forced': kwargs.get('forced', None)
        }
        data = {k: v for k, v in data.items() if v is not None}
        (resp, body) = https_client.api_call(method, endpoint, **{'data': data, 'headers': headers})
        return body

    @classmethod
    @register_cli_action('list_company_users', ('identifier',), ('',))
    def list_company_users(cls, https_client=get_gremlin_httpclient(), **kwargs):
        identifier = cls._error_if_not_identifier(**kwargs)
        endpoint = f'/companies/{identifier}/users'
        method = 'GET'
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

    @classmethod
    @register_cli_action('list_company_users', ('identifier', 'email',), ('body',))
    def update_company_user_role(cls, https_client=get_gremlin_httpclient(), **kwargs):
        identifier = cls._error_if_not_identifier(**kwargs)
        email = cls._error_if_not_email(**kwargs)
        endpoint = f'​/companies​/{identifier}​/users​/{email}'
        method = 'PUT'
        headers = https_client.header()
        data = kwargs.get('body', None)
        if data:
            (resp, body) = https_client.api_call(method, endpoint, **{'body': data, 'headers': headers})
        else:
            (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

    @classmethod
    @register_cli_action('activate_company_user', ('identifier', 'email',), ('',))
    def activate_company_user(cls, https_client=get_gremlin_httpclient(), **kwargs):
        identifier = cls._error_if_not_identifier(**kwargs)
        email = cls._error_if_not_email(**kwargs)
        endpoint = f'​/companies​/{identifier}​/users​/{email}​/active'
        method = 'POST'
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

    @classmethod
    @register_cli_action('deactivate_company_user', ('identifier', 'email',), ('',))
    def deactivate_company_user(cls, https_client=get_gremlin_httpclient(), **kwargs):
        identifier = cls._error_if_not_identifier(**kwargs)
        email = cls._error_if_not_email(**kwargs)
        endpoint = f'​/companies​/{identifier}​/users​/{email}​/active'
        method = 'DELETE'
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': headers})
        return body

