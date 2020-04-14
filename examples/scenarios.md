# Scenarios


## Create Scenarios

#### Example 1

Create and run a scenario that targets 50% of the containers owned by `kyle` with an escalating magnitude of 
100ms, 500ms, and 1000ms, then ramp the blast radius to 100% and repeat the magnitude escalation with a 5 second delay
between attacks.
```python
from gremlinapi.attack_helpers import *
from gremlinapi.scenario_helpers import *
from gremlinapi.scenarios import GremlinAPIScenarios as scenarios

my_scenario = GremlinScenarioHelper(name='test_scenario_1', description='My Test Scenario', hypothesis='No Hypothesis')

for blast_radius in [50, 100]:
    for magnatude in [100, 500, 1000]:
        my_scenario.add_step(
            GremlinILFIStep(
                delay=5,
                command=GremlinLatencyAttack(delay=magnatude),
                target=GremlinTargetContainers(strategy_type='Random', labels={'owner': 'kyle'}, percent=blast_radius)
            )
        )

my_scenario_guid = scenarios.create_scenario(body=my_scenario)
my_scenario_run = scenarios.run_scenario(guid=my_scenario_guid)
```

## Halt ScenarioS
```python
from gremlinapi.scenarios import GremlinAPIScenarios as scenarios
team_id = 'TEAM_ID/UUID'
scenario_id = 'SCENARIO_ID'
scenario_run = 'SCENARIO_RUN_ID'

confirmation = scenarios.halt_scenario(teamId=team_id, guid=scenario_id, runNumber=scenario_run)
```