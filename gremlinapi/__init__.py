# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Kyle Hultman <kyle@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import logging


from gremlinapi.alfi import GremlinALFI
from gremlinapi.attacks import GremlinAPIAttacks
from gremlinapi.clients import GremlinAPIClients
from gremlinapi.companies import GremlinAPICompanies
from gremlinapi.containers import GremlinAPIContainers
from gremlinapi.contracts import GremlinAPIContracts
from gremlinapi.exceptions import *
from gremlinapi.executions import GremlinAPIExecutions
from gremlinapi.gremlinapi import GremlinAPI
from gremlinapi.halts import GremlinAPIHalts
from gremlinapi.http_clients import get_gremlin_httpclient
from gremlinapi.kubernetes import GremlinAPIKubernetesAttacks, GremlinAPIKubernetesTargets
from gremlinapi.metadata import GremlinAPIMetadata
from gremlinapi.orgs import GremlinAPIOrgs
from gremlinapi.providers import GremlinAPIProviders
from gremlinapi.reports import GremlinAPIReports, GremlinAPIReportsSecurity
from gremlinapi.scenarios import GremlinAPIScenarios, GremlinAPIScenariosRecommended
from gremlinapi.schedules import GremlinAPISchedules
from gremlinapi.templates import GremlinAPITemplates
from gremlinapi.users import GremlinAPIUsers, GremlinAPIUsersAuth, GremlinAPIUsersAuthMFA
from gremlinapi.util import get_version


__version__ = get_version()


# Logging Configuration
logging.getLogger('GremlinAPI.client').addHandler(logging.StreamHandler())


# API Settings
_api_host = 'https://api.gremlin.com'
_api_version = 'v1'



