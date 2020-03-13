# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging

from gremlinapi.exceptions import (
    GremlinParameterError,
    ProxyError,
    ClientError,
    HTTPTimeout,
    HTTPError
)

from gremlinapi.cli import register_cli_action
from gremlinapi.http_clients import get_gremlin_httpclient


log = logging.getLogger('GremlinAPI.client')


class GremlinAPIContracts(object):

    @classmethod
    @register_cli_action('update_contract', ('identifier', 'body'), ('',))
    def update_contract(cls, https_client=get_gremlin_httpclient(), **kwargs):
        method = 'PATCH'
        identifier = kwargs.get('identifier', None)
        if not identifier:
            error_msg = f'Company identifier not supplied to update_contracts: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        data = kwargs.get('body', None)
        if not data:
            error_msg = f'Update body not supplied to update_contracts: {kwargs}'
            log.fatal(error_msg)
            raise GremlinParameterError(error_msg)
        endpoint = f'/companies/{identifier}/contracts/current'
        headers = https_client.header()
        (resp, body) = https_client.api_call(method, endpoint, **{'body': data, 'headers': headers})