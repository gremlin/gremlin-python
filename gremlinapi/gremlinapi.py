# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import json
import logging
import time

from gremlinapi.config import GremlinAPIConfig as config

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
        team_id = cls._info_if_not_param('teamId', **kwargs)
        if not team_id and type(config.team_id) is str:
            team_id = config.team_id
        if team_id:
            if '/?' in endpoint and not str(endpoint).endswith('?'):
                endpoint += f'&teamId={team_id}'
            elif '/?' in endpoint and (str(endpoint).endswith('?') or str(endpoint).endswith('&')):
                endpoint += f'teamId={team_id}'
            elif '/?' not in endpoint:
                endpoint += f'/?teamId={team_id}'
        return endpoint

    @classmethod
    def _error_if_not_json_body(cls, **kwargs):
        body = cls._warn_if_not_json_body(**kwargs)
        if not body:
            error_msg = f'JSON Body not supplied: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        return body

    @classmethod
    def _error_if_not_email(cls, **kwargs):
        email = cls._info_if_not_param('email', **kwargs)
        if not email:
            error_msg = f'email address not passed: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        # Do some email regex validation here...
        return email

    @classmethod
    def _error_if_not_param(cls, parameter_name, **kwargs):
        param = cls._info_if_not_param(parameter_name, **kwargs)
        if not param:
            error_msg = f'{parameter_name} not supplied: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        return param

    @classmethod
    def _info_if_not_param(cls, parameter_name, default=None, **kwargs):
        param = kwargs.get(parameter_name, None)
        if not param:
            error_msg = f'{parameter_name} not found in arguments: {kwargs}'
            log.info(error_msg)
            param = default
        return param

    @classmethod
    def _payload(cls, **kwargs):
        headers = kwargs.get('headers', None)
        body = kwargs.get('body', None)
        data = kwargs.get('data', None)
        payload = {'headers': headers, 'data': data, 'body': body}
        payload = {k: v for k, v in payload.items() if v is not None}
        return payload

    @classmethod
    def _warn_if_not_json_body(cls, **kwargs):
        body = cls._info_if_not_param('body', **kwargs)
        if not body:
            error_msg = f'JSON Body not supplied: {kwargs}'
            log.warning(error_msg)
        # Do some json validation
        return body

    @classmethod
    def _warn_if_not_param(cls, parameter_name, default=None, **kwargs):
        param = cls._info_if_not_param(parameter_name, **kwargs)
        if not param:
            error_msg = f'{parameter_name} not found in arguments: {kwargs}'
            log.warning(error_msg)
            param = default
        return param

