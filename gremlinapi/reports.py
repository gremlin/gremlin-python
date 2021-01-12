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
    HTTPError
)

from gremlinapi.gremlinapi import GremlinAPI
from gremlinapi.http_clients import get_gremlin_httpclient


log = logging.getLogger('GremlinAPI.client')


class GremlinAPIReports(GremlinAPI):
    @classmethod
    @register_cli_action('report_attacks', ('',), ('start', 'end', 'period', 'teamId'))
    def report_attacks(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        params = ['start', 'end', 'period']
        endpoint = cls._build_query_string_option_team_endpoint('/reports/attacks', params, **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('report_clients', ('',), ('start', 'end', 'period', 'teamId'))
    def report_clients(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        params = ['start', 'end', 'period']
        endpoint = cls._build_query_string_option_team_endpoint('/reports/clients', params, **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('report_companies', ('',), ('start', 'end', 'period', 'teamId'))
    def report_companies(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        params = ['startDate', 'endDate']
        endpoint = cls._build_query_string_endpoint('/reports/companies', params, **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    def report_pricing(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        params = ['startDate', 'endDate', 'trackingPeriod']
        endpoint = cls._build_query_string_endpoint('/reports/pricing', params, **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('report_teams', ('',), ('start', 'end', 'period', 'teamId'))
    def report_teams(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        params = ['startDate', 'endDate']
        endpoint = cls._build_query_string_option_team_endpoint('/reports/teams', params, **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

    @classmethod
    @register_cli_action('report_users', ('',), ('start', 'end', 'period', 'teamId'))
    def report_users(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        params = ['start', 'end', 'period']
        endpoint = cls._build_query_string_option_team_endpoint('/reports/users', params, **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

class GremlinAPIReportsSecurity(GremlinAPI):
    @classmethod
    @register_cli_action('report_security_access', ('start', 'end'), ('',))
    def report_security_access(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        params = ['start', 'end']
        endpoint = cls._build_query_string_endpoint('/reports/security/access', params, **kwargs)
        payload = cls._payload(**{'headers': https_client.header()})
        (resp, body) = https_client.api_call(method, endpoint, **payload)
        return body

