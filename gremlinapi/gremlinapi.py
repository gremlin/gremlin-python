# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

class GremlinAPI(object):

    def __init__(self):
        return

    @property
    def user(self):
        """Username for login"""
        return self._user

    @user.setter
    def user(self, user):
        self._user = user
        return self.user()

    @property
    def password(self):
        """Password for login"""
        return self._password

    @password.setter
    def password(self, password):
        self._password = password
        return self.password()

    