# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import json
import logging
import time

from gremlinapi.exceptions import (
    APIError,
    ProxyError,
    ClientError,
    HTTPTimeout,
    HTTPError
)

from gremlinapi.http_clients import get_gremlin_httpclient

log = logging.getLogger('GremlinAPI.client')


class GremlinAPI(object):
    def __init__(self):
        self._base_uri = 'https://api.gremlin.com/v1'

    @property
    def api_key(self):
        """API Key for API authorization"""
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        self._api_key = api_key
        return self.api_key

    @property
    def base_uri(self):
        return self._base_uri

    @base_uri.setter
    def base_uri(self, base_uri):
        self._base_uri = base_uri
        return self.base_uri

    @property
    def bearer_timestamp(self):
        return self._bearer_timestamp

    @bearer_timestamp.setter
    def bearer_timestamp(self, bearer_timestamp):
        self._bearer_timestamp = time.monotonic()

    @property
    def bearer_token(self):
        """Bearer token for API authorization"""
        return self._bearer_token

    @bearer_token.setter
    def bearer_token(self, bearer_token):
        self._bearer_token = bearer_token
        return self.bearer_token

    @property
    def company_name(self):
        """Company Name for login"""
        return self._company_name

    @company_name.setter
    def company_name(self, company_name):
        self._company_name = company_name
        return self.company_name

    @property
    def password(self):
        """Password for login"""
        return self._password

    @password.setter
    def password(self, password):
        self._password = password
        return self.password

    @property
    def user(self):
        """Username for login"""
        return self._user

    @user.setter
    def user(self, user):
        self._user = user
        return self.user

    """Will be moving the bulk of this logic to the GremlinAPIUsersAuth module"""
    @classmethod
    def login(cls, https_client = get_gremlin_httpclient()):
        if not cls.user and cls.password and cls.company_name:
            error_msg = f'Missing credentials; User: {cls.user}; Password: {cls.password}; Company: {cls.company_name}'
            log.fatal(error_msg)
            raise APIError(error_msg)

        uri = f'{cls.base_uri}/users/auth'
        payload = {"email": cls.user, "password": cls.password, "companyName"=cls.company_name}
        if(not cls.bearer_timestamp
           or not cls.bearer_token
           or (time.monotonic() - cls.bearer_timestamp >= cls.max_bearer_interval)):
            try:
                log.debug(f'Login API call to {uri} with payload {payload}')
                r = https_client.api_call('post', uri, data=payload)
                cls.bearer_timestamp = time.monotonic()
                cls.bearer_token = r.json()[0]['header']
                return r.json()[0]['header']
            except HTTPTimeout:
                time.sleep(1)
                cls.login()
            except ClientError:
                raise
            except ProxyError:
                raise
            except HTTPError:
                raise

        else:
            return cls.bearer_token
