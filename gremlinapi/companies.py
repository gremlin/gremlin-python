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
    @register_cli_action('get_company', ('identifier',), ('',))
    def get_company(cls, https_client=get_gremlin_httpclient(), **kwargs):
        method = 'GET'
        identifier = cls._error_if_not_param('identifier', **kwargs)
        endpoint = f'/companies/{identifier}'
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('list_company_clients', ('identifier',), ('',))
    def list_company_clients(cls, https_client=get_gremlin_httpclient(), **kwargs):
        method = 'GET'
        identifier = cls._error_if_not_param('identifier', **kwargs)
        endpoint = f'/companies/{identifier}/clients'
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('invite_company_user', ('identifier', 'body'), ('',))
    def invite_company_user(cls, https_client=get_gremlin_httpclient(), **kwargs):
        method = 'POST'
        identifier = cls._error_if_not_param('identifier', **kwargs)
        data = cls._error_if_not_json_body(**kwargs)
        if isinstance(data, dict):
            data = [dict(data)]
        endpoint = f'/companies/{identifier}/invites'
        payload = cls._payload(**{'headers': https_client.header(), 'body': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('delete_company_invite', ('identifier', 'email'), ('',))
    def delete_company_invite(cls, https_client=get_gremlin_httpclient(), **kwargs):
        method = 'DELETE'
        identifier = cls._error_if_not_param('identifier', **kwargs)
        email = cls._error_if_not_email(**kwargs)
        endpoint = f'/companies/{identifier}/invites/{email}'
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('company_mfa_prefs', ('identifier',), ('forceMfa', 'mfaProviders', 'defaultMfaProvider',))
    def company_mfa_prefs(cls, https_client=get_gremlin_httpclient(), **kwargs):
        method = 'POST'
        identifier = cls._error_if_not_param('identifier', **kwargs)
        data = {
            'forceMfa': cls._info_if_not_param('forceMfa', **kwargs),
            'mfaProviders': cls._info_if_not_param('mfaProviders', **kwargs),
            'defaultMfaProvider': cls._info_if_not_param('defaultMfaProvider', **kwargs)
        }
        data = {k: v for k, v in data.items() if v is not None}
        endpoint = f'/companies/{identifier}/mfaPrefs'
        payload = cls._payload(**{'headers': https_client.header(), 'data': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('update_company_prefs', ('identifier',), ('domain',))
    def update_company_prefs(cls, https_client=get_gremlin_httpclient(), **kwargs):
        method = 'POST'
        identifier = cls._error_if_not_param('identifier', **kwargs)
        data = {'domain': cls._info_if_not_param('domain', **kwargs)}
        data = {k: v for k, v in data.items() if v is not None}
        endpoint = f'/companies/{identifier}/prefs'
        payload = cls._payload(**{'headers': https_client.header(), 'data': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('update_company_saml_props',
                         ('identifier',),
                         ('enabled', 'entityId', 'idpUrl', 'certificate', 'forced'))
    def update_company_saml_props(cls, https_client=get_gremlin_httpclient(), **kwargs):
        method = 'POST'
        identifier = cls._error_if_not_param('identifier', **kwargs)
        data = {
            'enabled': cls._info_if_not_param('enabled', **kwargs),
            'entityId': cls._info_if_not_param('entityId', **kwargs),
            'idpUrl': cls._info_if_not_param('idpUrl', **kwargs),
            'certificate': cls._info_if_not_param('certificate', **kwargs),
            'forced': cls._info_if_not_param('forced', **kwargs)
        }
        data = {k: v for k, v in data.items() if v is not None}
        endpoint = f'/companies/{identifier}/saml/props'
        payload = cls._payload(**{'headers': https_client.header(), 'data': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('list_company_users', ('identifier',), ('',))
    def list_company_users(cls, https_client=get_gremlin_httpclient(), **kwargs):
        method = 'GET'
        identifier = cls._error_if_not_param('identifier', **kwargs)
        endpoint = f'/companies/{identifier}/users'
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('list_company_users', ('identifier', 'email',), ('body',))
    def update_company_user_role(cls, https_client=get_gremlin_httpclient(), **kwargs):
        method = 'PUT'
        identifier = cls._error_if_not_param('identifier', **kwargs)
        email = cls._error_if_not_email(**kwargs)
        data = cls._warn_if_not_json_body(**kwargs)
        endpoint = f'​/companies​/{identifier}​/users​/{email}'
        payload = cls._payload(**{'headers': https_client.header(), 'body': data})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('activate_company_user', ('identifier', 'email',), ('',))
    def activate_company_user(cls, https_client=get_gremlin_httpclient(), **kwargs):
        method = 'POST'
        identifier = cls._error_if_not_param('identifier', **kwargs)
        email = cls._error_if_not_email(**kwargs)
        endpoint = f'​/companies​/{identifier}​/users​/{email}​/active'
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('deactivate_company_user', ('identifier', 'email',), ('',))
    def deactivate_company_user(cls, https_client=get_gremlin_httpclient(), **kwargs):
        method = 'DELETE'
        identifier = cls._error_if_not_param('identifier', **kwargs)
        email = cls._error_if_not_email(**kwargs)
        endpoint = f'​/companies​/{identifier}​/users​/{email}​/active'
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

