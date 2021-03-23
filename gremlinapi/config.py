# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>


import logging

from datetime import datetime, timezone

from typing import Optional

log = logging.getLogger("GremlinAPI.client")


class GremlinAPIConfig(object):
    def __init__(self):
        self._api_key = None
        self._base_uri = None
        self._bearer_expires = None
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
    def api_key(self) -> Optional[str]:
        if not self._api_key:
            return None
        return self._api_key

    @api_key.setter
    def api_key(self, api_key: str):
        self._api_key = api_key
        return self.api_key

    @property
    def base_uri(self) -> str:
        return self._base_uri

    @base_uri.setter
    def base_uri(self, base_uri: str):
        self._base_uri = base_uri
        return self.base_uri

    @property
    def bearer_expires(self) -> datetime:
        return self._bearer_expires

    @bearer_expires.setter
    def bearer_expires(self, bearer_expires: datetime) -> None:
        """
        :param bearer_expires:
        :return:
        """
        self._bearer_expires = bearer_expires

    @property
    def bearer_timestamp(self) -> str:
        return self._bearer_timestamp

    @bearer_timestamp.setter
    def bearer_timestamp(self, bearer_timestamp: str) -> None:
        self._bearer_timestamp = bearer_timestamp

    @property
    def bearer_token(self) -> str:
        """Bearer token for API authorization"""
        return self._bearer_token

    @bearer_token.setter
    def bearer_token(self, bearer_token: str) -> str:
        self._bearer_token = bearer_token
        return self.bearer_token

    @property
    def company_name(self) -> str:
        """Company Name for login"""
        return self._company_name

    @company_name.setter
    def company_name(self, company_name: str) -> str:
        self._company_name = company_name
        return self.company_name

    @property
    def http_proxy(self) -> str:
        return self._http_proxy

    @http_proxy.setter
    def http_proxy(self, http_proxy: str) -> str:
        self._http_proxy = http_proxy
        return self.http_proxy

    @property
    def https_proxy(self) -> str:
        return self._https_proxy

    @https_proxy.setter
    def https_proxy(self, https_proxy: str) -> str:
        self._https_proxy = https_proxy
        return self.https_proxy

    @property
    def max_bearer_interval(self) -> int:
        return self._max_bearer_interval

    @max_bearer_interval.setter
    def max_bearer_interval(self, max_bearer_interval: int) -> int:
        self._max_bearer_interval = max_bearer_interval
        return self.max_bearer_interval

    @property
    def password(self) -> str:
        """Password for login"""
        return self._password

    @password.setter
    def password(self, password: str) -> str:
        self._password = password
        return self.password

    @property
    def team_id(self) -> str:
        return self._team_id

    @team_id.setter
    def team_id(self, team_id: str) -> str:
        self._team_id = team_id
        return self.team_id

    @property
    def user(self) -> str:
        """Username for login"""
        return self._user

    @user.setter
    def user(self, user: str) -> str:
        self._user = user
        return self.user

    @property
    def user_mfa_token_value(self) -> str:
        return self._user_mfa_token_value

    @user_mfa_token_value.setter
    def user_mfa_token_value(self, user_mfa_token_value: str) -> str:
        self._user_mfa_token_value = user_mfa_token_value
        return self.user_mfa_token_value

    @classmethod
    def is_bearer_expired(cls) -> bool:
        """
        Built-in to let the user check in the bearer token is expired
        Primarily used by the login function
        :return: bool
        """
        return datetime.now(timezone.utc) >= cls.bearer_expires  # type: ignore
