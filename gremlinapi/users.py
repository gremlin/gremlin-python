# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging



log = logging.getLogger('GremlinAPI.client')


class GremlinAPIUsers(object):

    def __init__(self):
        pass

    @classmethod
    def list_users(cls, https_client, **kwargs):
        pass

    @classmethod
    def invite_user(cls, https_client, **kwargs):
        pass

    @classmethod
    def delete_user(cls, https_client, **kwargs):
        pass

    @classmethod
    def update_user(cls, https_client, **kwargs):
        pass

class GremlinAPIUsersAuth(object):

    def __init__(self):
        pass

    @classmethod
    def auth_user(cls, https_client, **kwargs):
        pass

    @classmethod
    def auth_user_sso(cls, https_client, **kwargs):
        pass

    @classmethod
    def invalidate_session(cls, https_client, **kwargs):
        pass

    @classmethod
    def email_companies(cls, https_client, **kwargs):
        pass

    @classmethod
    def saml_metadata(cls, https_client, **kwargs):
        pass

class GremlinAPIUsersAuthMFA(object):
    pass