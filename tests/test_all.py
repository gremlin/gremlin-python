# -*- coding: utf-8 -*-

# Copyright (C) 2021 Kyle Bouchard <kyle.bouchard@gremlin.com>, Gremlin Inc <sales@gremlin.com>

import unittest

from .test_httpclient import TestHttpClient
from .test_attacks import TestAttacks
from .test_alfi import TestAlfi
from .test_apikeys import TestAPIKeys
from .test_attack_helpers import TestAttackHelpers
from .test_cli import TestCLI
from .test_clients import TestClients
from .test_companies import TestCompanies
from .test_containers import TestContainers
from .test_contracts import TestContracts
from .test_executions import TestExecutions
from .test_gremlinapi import TestAPI

if __name__ == "__main__":
    unittest.main()
