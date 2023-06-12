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
from .test_halts import TestHalts
from .test_kubernetes import TestKubernetesAttacks, TestKubernetesTargets
from .test_metadata import TestMetadata
from .test_metrics import TestMetrics
from .test_orgs import TestOrgs
from .test_oauth import TestOAUTH
from .test_providers import TestProviders
from .test_reports import TestReports
from .test_saml import TestSaml
from .test_scenario_graph_helpers import TestScenarioGraphHelpers
from .test_scenarios import TestScenarios
from .test_schedules import TestSchedules
from .test_users import TestUsers

# from .test_scenario_helpers import TestScenarioHelpers
# from .test_templates import TestTemplates


if __name__ == "__main__":
    unittest.main()
