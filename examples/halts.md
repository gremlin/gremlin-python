# Halts

### Halt all attacks

```python
from gremlinapi.halts import GremlinAPIHalts as halts
team_id = 'TEAM_ID/UUID'
halt_body = {'reason': 'Showing off how to halt attacks',
             'reference': 'Monitoring Dashboard ID'}

confirmation = halts.halt_all_attacks(teamId=team_id, body=halt_body)
```

## ALFI Endpoint
### Halt ALFI Experiment

```python
from gremlinapi.alfi import GremlinALFI as alfi

alfi_attack_id = 'expirment-guid'
alfi.halt_alfi_experiment(guid=alfi_attack_id)
```

### Halt _ALL_ ALFI Experiments

```python
from gremlinapi.alfi import GremlinALFI as alfi

alfi.halt_all_alfi_experiments()
```


## Attacks Endpoint
### Halt Attack

```python
from gremlinapi.attacks import GremlinAPIAttacks as attacks
team_id = 'TEAM_ID/UUID'
attack_id = 'ATTACK_ID'

confirmation = attacks.halt_attack(guid=attack_id, teamId=team_id)
```

### Halt _ALL_ Attacks

```python
from gremlinapi.attacks import GremlinAPIAttacks as attacks
team_id = 'TEAM_ID/UUID'

confirmation = attacks.halt_all_attacks(teamId=team_id)
```

## Kubernetes Endpoint
### Halt Kubernetes Attack
```python
from gremlinapi.kubernetes import GremlinAPIKubernetesAttacks as k8attacks
team_id = 'TEAM_ID/UUID'
attack_id = 'ATTACK_ID'

confirmation = k8attacks.halt_kubernetes_attack(guid=attack_id, teamId=team_id)
```

### Halt All Kubernetes Attacks
```python
from gremlinapi.kubernetes import GremlinAPIKubernetesAttacks as k8attacks
team_id = 'TEAM_ID/UUID'

confirmation = k8attacks.halt_all_kubernetes_attacks(teamId=team_id)
```

## Scenarios
### Halt Scenario
```python
from gremlinapi.scenarios import GremlinAPIScenarios as scenarios
team_id = 'TEAM_ID/UUID'
scenario_id = 'SCENARIO_ID'
scenario_run = 'SCENARIO_RUN_ID'

confirmation = scenarios.halt_scenario(teamId=team_id, guid=scenario_id, runNumber=scenario_run)
```