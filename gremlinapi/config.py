# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>


import logging

log = logging.getLogger('GremlinAPI.client')


class GremlinAPIConfig(object):

    def __init__(self):
        self._api_key = None
        self._base_uri = None
        self._bearer_timestamp = None
        self._bearer_token = None
        self._company_name = None
        self._http_proxy = False
        self._https_proxy = False
        self._max_bearer_interval = None
        self._password = None
        self._team_id = None
        self._user = None
        self._user_mfa_token_value = None

    @property
    def api_key(self):
        if not self._api_key:
            return None
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
    def http_proxy(self):
        return self._http_proxy

    @http_proxy.setter
    def http_proxy(self, http_proxy):
        self._http_proxy = http_proxy
        return self.http_proxy

    @property
    def https_proxy(self):
        return self._https_proxy

    @https_proxy.setter
    def https_proxy(self, https_proxy):
        self._https_proxy = https_proxy
        return self.https_proxy

    @property
    def max_bearer_interval(self):
        return self._max_bearer_interval

    @max_bearer_interval.setter
    def max_bearer_interval(self, max_bearer_interval):
        self._max_bearer_interval = max_bearer_interval
        return self.max_bearer_interval

    @property
    def password(self):
        """Password for login"""
        return self._password

    @password.setter
    def password(self, password):
        self._password = password
        return self.password

    @property
    def team_id(self):
        return self._team_id

    @team_id.setter
    def team_id(self, team_id):
        self._team_id = team_id
        return self.team_id

    @property
    def user(self):
        """Username for login"""
        return self._user

    @user.setter
    def user(self, user):
        self._user = user
        return self.user

    @property
    def user_mfa_token_value(self):
        return self._user_mfa_token_value

    @user_mfa_token_value.setter
    def user_mfa_token_value(self, user_mfa_token_value):
        self._user_mfa_token_value = user_mfa_token_value
        return self.user_mfa_token_value