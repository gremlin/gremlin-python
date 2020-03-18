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
    def _report_endpoint(cls, endpoint, **kwargs):
        start = kwargs.get('start', None)
        end = kwargs.get('end', None)
        period = kwargs.get('period', None)
        if start or end or period or team_id:
            endpoint += '/?'
            if start:
                endpoint += f'start={start}&'
            if end:
                endpoint += f'end={end}&'
            if period:
                endpoint += f'period={period}&'
        return cls._optional_team_endpoint(endpoint, **kwargs)

    @classmethod
    @register_cli_action('report_attacks', ('',), ('start', 'end', 'period', 'teamId'))
    def report_attacks(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._report_endpoint('/reports/attacks', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

    @classmethod
    @register_cli_action('report_clients', ('',), ('start', 'end', 'period', 'teamId'))
    def report_clients(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._report_endpoint('/reports/clients', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

    @classmethod
    @register_cli_action('report_companies', ('',), ('start', 'end', 'period', 'teamId'))
    def report_companies(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._report_endpoint('/reports/companies', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

    @classmethod
    @register_cli_action('report_teams', ('',), ('start', 'end', 'period', 'teamId'))
    def report_teams(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._report_endpoint('/reports/teams', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

    @classmethod
    @register_cli_action('report_users', ('',), ('start', 'end', 'period', 'teamId'))
    def report_users(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._report_endpoint('/reports/users', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

class GremlinAPIReportsSecurity(GremlinAPI):

    @classmethod
    def _report_endpoint(cls, endpoint, **kwargs):
        start = kwargs.get('start', str(date.today()))
        end = kwargs.get('end', str(date.today()))
        format = kwargs.get('format', 'JSON')
        endpoint += f'/?start={start}&end={end}&format={format}'
        return endpoint

    @classmethod
    def _team_report_endpoint(cls, endpoint, **kwargs):
        team_id = kwargs.get('teamId', None)
        if not team_id:
            error_msg = f'teamId not supplied to reports.security endpoint: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        endpoint += cls._report_endpoint(endpoint, **kwargs) + f'&teamId={team_id}'
        return endpoint

    @classmethod
    def _user_report_endpoint(cls, endpoint, **kwargs):
        email = kwargs.get('teamId', None)
        if not email:
            error_msg = f'userEmail not supplied to reports.security endpoint: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        endpoint += cls._report_endpoint(endpoint, **kwargs) + f'&userEmail={email}'
        return endpoint

    @classmethod
    @register_cli_action('report_security_access', ('start', 'end', 'format'), ('',))
    def report_security_access(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._report_endpoint('/reports/security/access', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

    @classmethod
    @register_cli_action('report_security_access_by_team', ('start', 'end', 'format', 'teamId'), ('',))
    def report_security_access_by_team(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._team_report_endpoint('/reports/security/accessByTeam', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

    @classmethod
    @register_cli_action('report_security_activity', ('start', 'end', 'format'), ('',))
    def report_security_activity(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._report_endpoint('/reports/security/activity', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

    @classmethod
    @register_cli_action('report_security_activity_by_team', ('start', 'end', 'format', 'teamId'), ('',))
    def report_security_activity_by_team(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._team_report_endpoint('/reports/security/activityByTeam', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

    @classmethod
    @register_cli_action('report_security_auth', ('start', 'end', 'format'), ('',))
    def report_security_auth(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._report_endpoint('/reports/security/auth', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

    @classmethod
    @register_cli_action('report_security_auth_by_team', ('start', 'end', 'format', 'teamId'), ('',))
    def report_security_auth_by_team(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._team_report_endpoint('/reports/security/authByTeam', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

    @classmethod
    @register_cli_action('report_security_denied_access', ('start', 'end', 'format'), ('',))
    def report_security_denied_access(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._report_endpoint('/reports/security/deniedAccess', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

    @classmethod
    @register_cli_action('report_security_denied_access_by_team', ('start', 'end', 'format', 'teamId'), ('',))
    def report_security_denied_access_by_team(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._team_report_endpoint('/reports/security/deniedAccessByTeam', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

    @classmethod
    @register_cli_action('report_security_denied_access_auth_endpoints', ('start', 'end', 'format'), ('',))
    def report_security_denied_access_auth_endpoints(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._report_endpoint('/reports/security/deniedAccessAuthEndpoints', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

    @classmethod
    @register_cli_action('report_security_denied_access_auth_endpoints_by_team',
                         ('start', 'end', 'format', 'teamId'), ('',))
    def report_security_denied_access_auth_enpoinds_by_team(cls, https_client=get_gremlin_httpclient(),
                                                            *args, **kwargs):
        method = 'GET'
        endpoint = cls._team_report_endpoint('/reports/security/deniedAccessAuthEndpointsByTeam', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

    @classmethod
    @register_cli_action('report_security_denied_user_access', ('start', 'end', 'format', 'userEmail'), ('',))
    def report_security_denied_user_access(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._user_report_endpoint('/reports/security/deniedUserAccess', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

    @classmethod
    @register_cli_action('report_security_denied_user_access_auth_endpoints',
                         ('start', 'end', 'format', 'userEmail'), ('',))
    def report_security_denied_user_access_auth_endpoints(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._user_report_endpoint('/reports/security/deniedUserAccessAuthEndpoints', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

    @classmethod
    @register_cli_action('report_security_user_access', ('start', 'end', 'format', 'userEmail'), ('',))
    def report_security_user_access(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._user_report_endpoint('/reports/security/userAccess', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

    @classmethod
    @register_cli_action('report_security_user_activity', ('start', 'end', 'format', 'userEmail'), ('',))
    def report_security_user_activity(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._user_report_endpoint('/reports/security/userActivity', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

    @classmethod
    @register_cli_action('report_security_user_auth', ('start', 'end', 'format', 'userEmail'), ('',))
    def report_security_user_auth(cls, https_client=get_gremlin_httpclient(), *args, **kwargs):
        method = 'GET'
        endpoint = cls._user_report_endpoint('/reports/security/userAuth', **kwargs)
        header = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'headers': header})
        return body

