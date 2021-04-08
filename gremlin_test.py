import logging
import os

# logging_levels = {
#     'CRITICAL': logging.CRITICAL,
#     'ERROR': logging.ERROR,
#     'WARNING': logging.WARNING,
#     'INFO': logging.INFO,
#     'DEBUG': logging.DEBUG
# }

# log = logging.getLogger('testscript')
# log_handler = logging.StreamHandler()
# log_formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
# log_handler.setFormatter(log_formatter)
# log.addHandler(log_handler)
# log.setLevel(logging_levels.get(os.getenv('GREMLIN_PYTHON_API_LOG_LEVEL', 'DEBUG'), logging.WARNING))

# log.error("error message")
# if (log.getEffectiveLevel() == logging.DEBUG): log.debug("debug message")
# else: print("debug mode off")
# log.fatal("fatal message")
# log.info("info message")
# log.warning("warning message")

import gremlinapi
from gremlinapi.users import GremlinAPIUsers
from gremlinapi.companies import GremlinAPICompanies
from gremlinapi.containers import GremlinAPIContainers
from gremlinapi.attacks import GremlinAPIAttacks
from gremlinapi.attack_helpers import (
    GremlinLatencyAttack,
    GremlinTargetContainers,
    GremlinCPUAttack,
    GremlinBlackholeAttack,
)
from gremlinapi.config import GremlinAPIConfig as config
from gremlinapi.scenarios import GremlinAPIScenarios

# from gremlinapi.scenario_helpers import GremlinScenarioHelper, GremlinILFIStep
from gremlinapi.scenario_graph_helpers import (
    GremlinScenarioGraphHelper,
    GremlinScenarioILFINode,
    GremlinScenarioStatusCheckNode,
    GremlinScenarioDelayNode,
)

GREMLIN_COMPANY = "Hooli"
GREMLIN_USER = "kyle.bouchard+demo@gremlin.com"
GREMLIN_PASSWORD = "***REMOVED***"
GREMLIN_PYTHON_API_LOG_LEVEL = "DEBUG"
hooli_id = "9676868b-60d2-5ebe-aa66-c1de8162ff9d"

config.api_key = "f4aef9e8d11bcb286c06bd2125b2eb6189b3af77829773d5a8fa2a3fdbc8f71c"
config.team_id = hooli_id

gremlinapi.login(
    email=GREMLIN_USER,
    password=GREMLIN_PASSWORD,
    company_name=GREMLIN_COMPANY,
)

# gK8sTargets = GremlinAPIContainers.list_containers()
# for target in gK8sTargets:
#     print(target)

# gScenarios = GremlinAPIScenarios.list_scenarios(teamId=hooli_id)
# for scenario in gScenarios:
#     if scenario["guid"] == "1563bf99-a75a-4981-a3bf-99a75a79810e":
#         print("---")
#         print(scenario)
#         print("---")

# Status check config
status_check_description = "Check if Gremlin.com is Still Up"

endpoint_url = "https://www.google.com"
endpoint_headers = dict()

# Optionally you can set specific header attributes
# status_check_api_key = 'Key foo...'
endpoint_headers = {"Authorization": config.api_key}

evaluation_ok_status_codes = ["404", "300"]
evaluation_ok_latency_max = 1000
evaluation_response_body_evaluation = {"op": "AND", "predicates": []}

blast_radius = 100
delay_time = 5  # Time to delay between steps in seconds
my_scenario = GremlinScenarioGraphHelper(
    name="code_created_scenario_postgraph_rev2",
    description="Python Code updated scenario for testing namespace changes",
    hypothesis="No Hypothesis",
)

# Add the status check to the start of the scenario
new_node = GremlinScenarioStatusCheckNode(
    description=status_check_description,
    endpoint_url=endpoint_url,
    endpoint_headers=endpoint_headers,
    evaluation_ok_status_codes=evaluation_ok_status_codes,
    evaluation_ok_latency_max=evaluation_ok_latency_max,
    evaluation_response_body_evaluation=evaluation_response_body_evaluation,
)
my_scenario.add_node(new_node, True)
# my_scenario.add_edge(new_node)
new_node = GremlinScenarioStatusCheckNode(
    description=status_check_description,
    endpoint_url=endpoint_url,
    endpoint_headers=endpoint_headers,
    evaluation_ok_status_codes=evaluation_ok_status_codes,
    evaluation_ok_latency_max=evaluation_ok_latency_max,
    evaluation_response_body_evaluation=evaluation_response_body_evaluation,
)
my_scenario.add_node(new_node, True)
# my_scenario.add_edge(new_node)
new_node = GremlinScenarioILFINode(
    command=GremlinBlackholeAttack(),
    target=GremlinTargetContainers(
        strategy_type="Random", labels={"owner": "kyle"}, percent=blast_radius
    ),
)
my_scenario.add_node(new_node, True)
# my_scenario.add_edge(new_node)
# Add a delay step between the status check and the attacks
new_node = GremlinScenarioDelayNode(description="Add some delay", delay=delay_time)
my_scenario.add_node(new_node, True)
# my_scenario.add_edge(new_node)
new_node = GremlinScenarioStatusCheckNode(
    description=status_check_description,
    endpoint_url=endpoint_url,
    endpoint_headers=endpoint_headers,
    evaluation_ok_status_codes=evaluation_ok_status_codes,
    evaluation_ok_latency_max=evaluation_ok_latency_max,
    evaluation_response_body_evaluation=evaluation_response_body_evaluation,
)
my_scenario.add_node(new_node, True)
# my_scenario.add_edge(new_node)

# blast_radius = 75
# magnatude = 500

# my_scenario.add_node(
#     GremlinScenarioILFINode(
#         command=GremlinCPUAttack(delay=magnatude),
#         target=GremlinTargetContainers(strategy_type='Random', labels={'owner': 'kyleb'}, percent=blast_radius)
#     )
# )


test_body_2 = {
    "org_id": "9676868b-60d2-5ebe-aa66-c1de8162ff9d",
    "guid": "1563bf99-a75a-4981-a3bf-99a75a79810e",
    "name": "code_created_scenario",
    "description": "Python Code updated manually scenario for testing namespace changes",
    "hypothesis": "No Hypothesis",
    "graph": {
        "nodes": {
            "0": {
                "thirdPartyPresets": "PythonSDK",
                "endpointConfiguration": {
                    "url": "https://www.google.com",
                    "headers": {
                        "Authorization": "f4aef9e8d11bcb286c06bd2125b2eb6189b3af77829773d5a8fa2a3fdbc8f71c"
                    },
                },
                "evaluationConfiguration": {
                    "okLatencyMaxMs": 1000,
                    "okStatusCodes": ["404", "300"],
                    "responseBodyEvaluation": {"op": "AND", "predicates": []},
                },
                "type": "SynchronousStatusCheck",
                "id": "0",
                "next": "1",
                "state": {"lifecycle": "NotStarted"},
                "guid": "c25e548f-6869-408b-9e54-8f6869e08b19",
            },
            "1": {
                "thirdPartyPresets": "PythonSDK",
                "endpointConfiguration": {
                    "url": "https://www.google.com",
                    "headers": {
                        "Authorization": "f4aef9e8d11bcb286c06bd2125b2eb6189b3af77829773d5a8fa2a3fdbc8f71c"
                    },
                },
                "evaluationConfiguration": {
                    "okLatencyMaxMs": 1000,
                    "okStatusCodes": ["404", "300"],
                    "responseBodyEvaluation": {"op": "AND", "predicates": []},
                },
                "type": "SynchronousStatusCheck",
                "id": "1",
                "next": "2",
                "state": {"lifecycle": "NotStarted"},
                "guid": "e9b19c26-aa6f-411c-b19c-26aa6f911c58",
            },
            "2": {
                "delay": 5,
                "type": "Delay",
                "id": "2",
                "next": "3",
                "state": {"lifecycle": "NotStarted"},
                "guid": "6195dd59-0c43-49d3-95dd-590c4379d3a2",
            },
            "3": {
                "target_definition": {
                    "k8s_objects": [
                        {
                            "uid": "15df3bca-bbc4-42d1-af77-bd1461cdec2c",
                            "labels": {},
                            "annotations": {},
                            "targetType": "Kubernetes",
                        }
                    ],
                    "strategy_type": "Random",
                    "target_type": "Kubernetes",
                    "strategy": {
                        "percentage": 100,
                        "attrs": {},
                        "type": "RandomPercent",
                    },
                },
                "impact_definition": {
                    "infra_command_type": "blackhole",
                    "infra_command_args": {
                        "hostnames": "^api.gremlin.com",
                        "egress_ports": "^53",
                        "providers": [],
                        "type": "blackhole",
                        "length": 60,
                        "cli_args": [
                            "blackhole",
                            "-l",
                            "60",
                            "-h",
                            "^api.gremlin.com",
                            "-p",
                            "^53",
                        ],
                    },
                },
                "attack_configuration": {
                    "command": {
                        "infraCommandType": "blackhole",
                        "infraCommandArgs": {
                            "hostnames": "^api.gremlin.com",
                            "egress_ports": "^53",
                            "providers": [],
                            "type": "blackhole",
                            "length": 60,
                            "cli_args": [
                                "blackhole",
                                "-l",
                                "60",
                                "-h",
                                "^api.gremlin.com",
                                "-p",
                                "^53",
                            ],
                        },
                    },
                    "targets": [
                        {
                            "targetingStrategy": {
                                "type": "Kubernetes",
                                "ids": ["15df3bca-bbc4-42d1-af77-bd1461cdec2c"],
                                "containerSelection": {"selectionType": "ANY"},
                            }
                        }
                    ],
                    "sampling": {"type": "Even", "percent": 100},
                },
                "type": "InfraAttack",
                "id": "3",
                "next": "4",
                "state": {"lifecycle": "NotStarted"},
                "guid": "d5752655-0a02-4137-b526-550a02d13757",
            },
            "4": {
                "delay": 5,
                "type": "Delay",
                "id": "4",
                "next": "5",
                "state": {"lifecycle": "NotStarted"},
                "guid": "c6b6210e-1a98-4429-b621-0e1a9864290d",
            },
            "5": {
                "thirdPartyPresets": "PythonSDK",
                "endpointConfiguration": {
                    "url": "https://www.google.com",
                    "headers": {
                        "Authorization": "f4aef9e8d11bcb286c06bd2125b2eb6189b3af77829773d5a8fa2a3fdbc8f71c"
                    },
                },
                "evaluationConfiguration": {
                    "okLatencyMaxMs": 1000,
                    "okStatusCodes": ["404", "300"],
                    "responseBodyEvaluation": {"op": "AND", "predicates": []},
                },
                "type": "SynchronousStatusCheck",
                "id": "5",
                "state": {"lifecycle": "NotStarted"},
                "guid": "56256bb3-93a5-4fd0-a56b-b393a52fd085",
            },
        },
        "start_id": "0",
    },
    "state": "DRAFT",
    "create_source": "GremlinSdkPython",
    "created_by": "kyle.bouchard+demo@gremlin.com",
    "created_at": "2021-03-31T15:33:55.090Z",
    "updated_at": "2021-03-31T18:48:11.080Z",
    "tiers": ["Free", "Enterprise"],
}

my_scenario_json_old = {
    "description": "Python Code updated scenario for testing namespace changes",
    "hypothesis": "No Hypothesis",
    "name": "code_created_scenario_postgraph",
    "graph": {
        "start_id": "status-check-18da56c3-8c91-4afe-8d4a-30c6d682e58e",
        "nodes": {
            "status-check-18da56c3-8c91-4afe-8d4a-30c6d682e58e": {
                "type": "SynchronousStatusCheck",
                "id": "status-check-18da56c3-8c91-4afe-8d4a-30c6d682e58e",
                "endpointConfiguration": {
                    "url": "https://www.google.com",
                    "headers": {
                        "Authorization": "f4aef9e8d11bcb286c06bd2125b2eb6189b3af77829773d5a8fa2a3fdbc8f71c"
                    },
                },
                "evaluationConfiguration": {
                    "okStatusCodes": ["404", "300"],
                    "okLatencyMaxMs": 1000,
                    "responseBodyEvaluation": {"op": "AND", "predicates": []},
                },
                "thirdPartyPresets": "PythonSDK",
            },
            "status-check-b7d0496a-b9be-45d6-bce8-32c5fbc1edd7": {
                "type": "SynchronousStatusCheck",
                "id": "status-check-b7d0496a-b9be-45d6-bce8-32c5fbc1edd7",
                "endpointConfiguration": {
                    "url": "https://www.google.com",
                    "headers": {
                        "Authorization": "f4aef9e8d11bcb286c06bd2125b2eb6189b3af77829773d5a8fa2a3fdbc8f71c"
                    },
                },
                "evaluationConfiguration": {
                    "okStatusCodes": ["404", "300"],
                    "okLatencyMaxMs": 1000,
                    "responseBodyEvaluation": {"op": "AND", "predicates": []},
                },
                "thirdPartyPresets": "PythonSDK",
            },
            "blackhole-58a4cc42-5330-41f6-8c35-457f31d7ee4c": {
                "type": "InfraAttack",
                "id": "blackhole-58a4cc42-5330-41f6-8c35-457f31d7ee4c",
                "impact_definition": {
                    "infra_command_args": {
                        "cli_args": [
                            "blackhole",
                            "-l",
                            "60",
                            "-p",
                            "^53",
                            "-h",
                            "^api.gremlin.com",
                        ],
                        "type": "blackhole",
                    },
                    "infra_command_type": "blackhole",
                },
                "target_definition": {
                    "strategy_type": "Random",
                    "strategy": {
                        "type": "RandomPercent",
                        "percentage": 100,
                        "attrs": {"multiSelectLabels": {"owner": ["kyle"]}},
                    },
                    "target_type": "Container",
                },
            },
            "Delay-dfe867cb-fe5f-4356-80e7-87211c27e8b6": {
                "type": "Delay",
                "id": "Delay-dfe867cb-fe5f-4356-80e7-87211c27e8b6",
                "delay": 5,
            },
            "status-check-bce5b32c-f458-4b09-bdc4-d5c6b8d5e086": {
                "type": "SynchronousStatusCheck",
                "id": "status-check-bce5b32c-f458-4b09-bdc4-d5c6b8d5e086",
                "endpointConfiguration": {
                    "url": "https://www.google.com",
                    "headers": {
                        "Authorization": "f4aef9e8d11bcb286c06bd2125b2eb6189b3af77829773d5a8fa2a3fdbc8f71c"
                    },
                },
                "evaluationConfiguration": {
                    "okStatusCodes": ["404", "300"],
                    "okLatencyMaxMs": 1000,
                    "responseBodyEvaluation": {"op": "AND", "predicates": []},
                },
                "thirdPartyPresets": "PythonSDK",
            },
        },
    },
}

my_scenario_json_new = {
    "description": "Python Code updated scenario for testing namespace changes",
    "hypothesis": "No Hypothesis",
    "name": "code_created_scenario_postgraph_rev2",
    "graph": {
        "start_id": "status-check-c430e7a8-65ab-4753-be16-85d403c1b8ba",
        "nodes": {
            "0": {
                "type": "SynchronousStatusCheck",
                "id": "status-check-c430e7a8-65ab-4753-be16-85d403c1b8ba",
                "endpointConfiguration": {
                    "url": "https://www.google.com",
                    "headers": {"Authorization": "...f71c"},
                },
                "evaluationConfiguration": {
                    "okStatusCodes": ["404", "300"],
                    "okLatencyMaxMs": 1000,
                    "responseBodyEvaluation": {"op": "AND", "predicates": []},
                },
                "thirdPartyPresets": "PythonSDK",
            },
            "1": {
                "type": "SynchronousStatusCheck",
                "id": "status-check-9ab6c327-560a-43d0-bfff-a808ff4b1a3e",
                "endpointConfiguration": {
                    "url": "https://www.google.com",
                    "headers": {"Authorization": "...f71c"},
                },
                "evaluationConfiguration": {
                    "okStatusCodes": ["404", "300"],
                    "okLatencyMaxMs": 1000,
                    "responseBodyEvaluation": {"op": "AND", "predicates": []},
                },
                "thirdPartyPresets": "PythonSDK",
            },
            "2": {
                "type": "InfraAttack",
                "id": "blackhole-917a0e53-db12-4949-81f8-2766506ddf80",
                "impact_definition": {
                    "infra_command_args": {
                        "cli_args": [
                            "blackhole",
                            "-l",
                            "60",
                            "-p",
                            "^53",
                            "-h",
                            "^api.gremlin.com",
                        ],
                        "type": "blackhole",
                    },
                    "infra_command_type": "blackhole",
                },
                "target_definition": {
                    "strategy_type": "Random",
                    "strategy": {
                        "type": "RandomPercent",
                        "percentage": 100,
                        "attrs": {"multiSelectLabels": {"owner": ["kyle"]}},
                    },
                    "target_type": "Container",
                },
            },
            "3": {
                "type": "Delay",
                "id": "Delay-c924e4bb-8eed-4a3f-acf1-0cf2e58039e4",
                "delay": 5,
            },
            "4": {
                "type": "SynchronousStatusCheck",
                "id": "status-check-fddb0d1c-9553-45e4-a28e-a3a967ed916c",
                "endpointConfiguration": {
                    "url": "https://www.google.com",
                    "headers": {"Authorization": "...f71c"},
                },
                "evaluationConfiguration": {
                    "okStatusCodes": ["404", "300"],
                    "okLatencyMaxMs": 1000,
                    "responseBodyEvaluation": {"op": "AND", "predicates": []},
                },
                "thirdPartyPresets": "PythonSDK",
            },
        },
    },
}


# GremlinAPIScenarios.update_scenario(
#     guid="1563bf99-a75a-4981-a3bf-99a75a79810e", body=test_body_2
# )
print(my_scenario)
GremlinAPIScenarios.create_scenario(body=my_scenario)
