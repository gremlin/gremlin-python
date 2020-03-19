# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>


import logging

log = logging.getLogger('GremlinAPI.client')


class GremlinAPIConfig(object):
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
    def team_guid(self):
        return self._team_guid

    @team_guid.setter
    def team_guid(self, team_guid):
        self._team_guid = team_guid
        return self.team_guid

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