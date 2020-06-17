# Scenarios


## Create Scenarios

### Graph Scenarios

#### Example

```python
from gremlinapi.config import GremlinAPIConfig as config
from gremlinapi.attack_helpers import GremlinBlackholeAttack, GremlinLatencyAttack, GremlinTargetContainers
from gremlinapi.scenario_graph_helpers import (GremlinScenarioGraphHelper, GremlinScenarioILFINode,
                                               GremlinScenarioDelayNode, GremlinScenarioStatusCheckNode)
from gremlinapi.scenarios import GremlinAPIScenarios as scenarios

my_api_key = "123...xyz"
my_team_guid = 'uuid'

config.api_key = my_api_key
config.team_guid = my_team_guid

description = f'This is a test scenario to illustrate the usage of the new scenario graph model'
hypothesis = f'This should create a functional scenario with multiple attack iterations and a status_check'

blast_radius_steps = [50, 100]  # Percents
latency_magnitude_steps = [100, 500, 1000]  # Latency in milliseconds
delay_time = 5 # Time to delay between steps in seconds

# Status check config
status_check_description="Check if Gremlin.com is Still Up"

endpoint_url = 'https://www.gremlin.com'
endpoint_headers = dict()

# Optionally you can set specific header attributes
# status_check_api_key = 'Key foo...'
# endpoint_headers = {
#     'Authorization': status_check_api_key
# }

evaluation_ok_status_codes = ['200-203', '210']
evaluation_ok_latency_max = 500
evaluation_response_body_evaluation = {
    "op": "AND",
    "predicates": []
}

my_scenario = GremlinScenarioGraphHelper(name='test_scenario_1', description=description, hypothesis=hypothesis)

# Add the status check to the start of the scenario
my_scenario.add_node(
    GremlinScenarioStatusCheckNode(
        description=status_check_description,
        endpoint_url=endpoint_url,
        endpoint_headers=endpoint_headers,
        evaluation_ok_status_codes=evaluation_ok_status_codes,
        evaluation_ok_latency_max=evaluation_ok_latency_max,
        evaluation_response_body_evaluation=evaluation_response_body_evaluation))

# Add a delay step between the status check and the attacks
my_scenario.add_node(GremlinScenarioDelayNode(delay=delay_time))

# Add latency attacks to the scenario
for magnitude_idx, magnitude in enumerate(latency_magnitude_steps):
    for blast_radius_idx, blast_radius in enumerate(blast_radius_steps):
        print(f'Blast radius {blast_radius_idx+1} of {len(blast_radius_steps)} :: {blast_radius}%')
        print(f'Magnitude {magnitude_idx+1} of {len(latency_magnitude_steps)} :: {magnitude}ms')
        my_scenario.add_node(
            GremlinScenarioILFINode(
                command=GremlinLatencyAttack(delay=magnitude),
                target=GremlinTargetContainers(strategy_type='Random', labels={'owner': 'kyle'}, percent=blast_radius)))
        # Add a delay step between attacks, skip this if it's the last step in the loop
        if not ((magnitude_idx+1 == len(latency_magnitude_steps)) and (blast_radius_idx+1 == len(blast_radius_steps))):
            my_scenario.add_node(GremlinScenarioDelayNode(delay=delay_time))

# Let's view the json output
print(my_scenario)

# Send the scenario to Gremlin
my_scenario_guid = scenarios.create_scenario(body=my_scenario)
```

### Step Scenarios (old)

#### Example

Create and run a scenario that targets 50% of the containers owned by `kyle` with an escalating magnitude of 
100ms, 500ms, and 1000ms, then ramp the blast radius to 100% and repeat the magnitude escalation with a 5 second delay
between attacks.
```python
from gremlinapi.attack_helpers import *
from gremlinapi.scenario_helpers import *
from gremlinapi.scenarios import GremlinAPIScenarios as scenarios

my_scenario = GremlinScenarioHelper(name='test_scenario_1', description='My Test Scenario', hypothesis='No Hypothesis')

for blast_radius in [50, 100]:
    for magnitude in [100, 500, 1000]:
        my_scenario.add_step(
            GremlinILFIStep(
                delay=5,
                command=GremlinLatencyAttack(delay=magnitude),
                target=GremlinTargetContainers(strategy_type='Random', labels={'owner': 'kyle'}, percent=blast_radius)
            )
        )

my_scenario_guid = scenarios.create_scenario(body=my_scenario)
my_scenario_run = scenarios.run_scenario(guid=my_scenario_guid)
```

## Halt Scenarios
```python
from gremlinapi.scenarios import GremlinAPIScenarios as scenarios
team_id = 'TEAM_ID/UUID'
scenario_id = 'SCENARIO_ID'
scenario_run = 'SCENARIO_RUN_ID'

confirmation = scenarios.halt_scenario(teamId=team_id, guid=scenario_id, runNumber=scenario_run)
```