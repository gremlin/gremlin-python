# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging

from gremlinapi.cli import register_cli_action

from gremlinapi.http_clients import get_gremlin_httpclient
from gremlinapi.config import GremlinAPIConfig

log = logging.getLogger('GremlinAPI.client')


class GremlinAPIUsers(object):

    def __init__(self):
        pass

    @classmethod
    def list_users(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    def invite_user(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    def delete_user(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    def update_user(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

class GremlinAPIUsersAuth(object):

    def __init__(self):
        pass

    @classmethod
    def auth_user(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    def auth_user_sso(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    def invalidate_session(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    def email_companies(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

    @classmethod
    def saml_metadata(cls, https_client=get_gremlin_httpclient(), **kwargs):
        pass

class GremlinAPIUsersAuthMFA(object):
    @classmethod
    @register_cli_action
    def auth_user(cls, https_client=get_gremlin_httpclient(), **kwargs):
        print(GremlinAPIConfig.base_uri)