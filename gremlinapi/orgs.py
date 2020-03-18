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


class GremlinAPIOrgs(GremlinAPI):

    @classmethod
    @register_cli_action('list_orgs', ('',), ('',))
    def list_orgs(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = '/orgs'
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

    @classmethod
    @register_cli_action('get_org', ('identifier',), ('',))
    def get_org(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        identifier = kwargs.get('identifier', None)
        if not identifier:
            error_msg = f'Organization identifier not provided to org endpoint: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        endpoint = f'/orgs/{identifier}'
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

    @classmethod
    @register_cli_action('create_org', ('body',), ('',))
    def create_org(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        endpoint = '/orgs'
        data = kwargs.get('body', None)
        if not data:
            error_msg = f'JSON body not provided to org endpoint, create_org: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'body': data, 'headers': header})
        return body

    @classmethod
    @register_cli_action('new_certificate', ('',), ('teamId',))
    def new_certificate(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        endpoint = cls._optional_team_endpoint('/orgs/auth/certificate', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

    @classmethod
    @register_cli_action('delete_certificate', ('',), ('teamId',))
    def delete_certificate(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'DELETE'
        endpoint = cls._optional_team_endpoint('/orgs/auth/certificate', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

    @classmethod
    @register_cli_action('delete_old_certificate', ('',), ('teamId',))
    def delete_old_certificate(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'DELETE'
        endpoint = cls._optional_team_endpoint('/orgs/auth/certificate/old', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

    @classmethod
    @register_cli_action('reset_secret', ('',), ('identifier', 'teamId'))
    def reset_secret(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'POST'
        endpoint = cls._optional_team_endpoint('/orgs/auth/secret/reset', **kwargs)
        data = dict()
        identifier = kwargs.get('identifier', None)
        if identifier:
            data['identifier'] = identifier
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'data': data, 'headers': header})
        return body

