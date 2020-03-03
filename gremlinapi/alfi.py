# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import json
import logging

from gremlinapi.exceptions import (
    ProxyError,
    ClientError,
    HTTPTimeout,
    HTTPError
)

from gremlinapi.http_clients import get_gremlin_httpclient

log = logging.getLogger('GremlinAPI.client')



class GremlinALFI(object):

    def __init__(self):
        return

    """
    Creates a new application level experiment.

    Authorization Schema Bearer Tokens Role Based Access Control TEAM_DEFAULT
    
    Traditional User
    
    API Keys Parameters Name Description body (body)
    string Parameter content type
    
    teamId (query)
    Required when using company session token (RBAC only).
    
    Responses Response content type
    
    Code Description 201
    successful operation string 400
    Bad Request 401
    ApiKey Invalid 403
    User requires privilege for target team: TEAM_DEFAULT
    """
    def experiments(self):
        return

