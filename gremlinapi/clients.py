# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging



log = logging.getLogger('GremlinAPI.client')


class GremlinAPIClients(object):

    def __init__(self):
        pass

    @classmethod
    def activate_client(cls, https_client, **kwargs):
        pass

    @classmethod
    def deactivate_client(cls, https_client, **kwargs):
        pass

    @classmethod
    def list_active_client(cls, https_client, **kwargs):
        pass

    @classmethod
    def list_clients(cls, https_client, **kwargs):
        pass