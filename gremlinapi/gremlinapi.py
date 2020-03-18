# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import json
import logging
import time

from gremlinapi.exceptions import (
    APIError,
    GremlinParameterError,
    ProxyError,
    ClientError,
    HTTPTimeout,
    HTTPError
)

from gremlinapi.http_clients import get_gremlin_httpclient

log = logging.getLogger('GremlinAPI.client')


class GremlinAPI(object):
    def __init__(self):
        pass

    @classmethod
    def _optional_team_endpoint(cls, endpoint, **kwargs):
        team_id = kwargs.get('teamId', None)
        if team_id:
            if '/?' in endpoint and not str(endpoint).endswith('?'):
                endpoint += f'&teamId={team_id}'
            elif '/?' in endpoint and (str(endpoint).endswith('?') or str(endpoint).endswith('&')):
                endpoint += f'teamId={team_id}'
            elif '/?' not in endpoint:
                endpoint += f'/?teamId={team_id}'
        return endpoint

    @classmethod
    def _error_if_not_body(cls, **kwargs):
        body = kwargs.get('body', None)
        if not body:
            error_msg = f'JSON Body not supplied: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        return body

    @classmethod
    def _error_if_not_email(cls, **kwargs):
        email = kwargs.get('email', None)
        if not email:
            error_msg = f'email address not passed: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        return email

    @classmethod
    def _error_if_not_guid(cls, **kwargs):
        guid = kwargs.get('guid', None)
        if not guid:
            error_msg = f'GUID parameter not supplied: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        return guid

    @classmethod
    def _error_if_not_identifier(cls, **kwargs):
        identifier = kwargs.get('identifier', None)
        if not identifier:
            error_msg = f'Company identifier not supplied correctly: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        return identifier

    @classmethod
    def _error_if_not_team_id(cls, **kwargs):
        team_id = kwargs.get('teamId', None)
        if not team_id:
            error_msg = f'teamId required parameter not supplied: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        return team_id

    @classmethod
    def _payload(cls, **kwargs):
        headers = kwargs.get('headers', None)
        body = kwargs.get('body', None)
        data = kwargs.get('data', None)
        payload = {'headers': headers, 'data': data, 'body': body}
        payload = {k: v for k, v in payload.items() if v is not None}
        return payload


    @classmethod
    def _warn_if_not_body(cls, **kwargs):
        body = kwargs.get('body', None)
        if not body:
            error_msg = f'JSON Body not supplied: {kwargs}'
            log.warning(error_msg)
        return body

