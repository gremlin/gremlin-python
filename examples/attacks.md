# Attacks

## Create Attacks

Creating attacks with the 

#### Resource Attacks

##### CPU

This will target 100% of all containers with the container label of `owner: 'kyle'` for five minute
```python
from gremlinapi.attacks import GremlinAPIAttacks as attacks
from gremlinapi.attack_helpers import GremlinAttackHelper, GremlinTargetContainers, GremlinCPUAttack

attacks.create_attack(
    body=GremlinAttackHelper(
        target=GremlinTargetContainers(type='Random', labels={'owner': 'kyle'}, percent=100),
        command=GremlinCPUAttack(length=300, all_cores=True, capacity=100)))
```

##### Memory

This will target 10% of all hosts with a memory attack of 75% Memory per host for one minute
```python
from gremlinapi.attacks import GremlinAPIAttacks as attacks
from gremlinapi.attack_helpers import GremlinAttackHelper, GremlinTargetHosts, GremlinMemoryAttack
attacks.create_attack(body=GremlinAttackHelper(target=GremlinTargetHosts(), command=GremlinMemoryAttack()))
```

##### Disk Space

Long format example targeting 3 hosts with a disk fill attack
```python
from gremlinapi.attacks import GremlinAPIAttacks as attacks
from gremlinapi.attack_helpers import GremlinAttackHelper, GremlinTargetHosts, GremlinDiskSpaceAttack

atk_targets = GremlinTargetHosts(
    type='Exact',
    ids=[
        '10.189.7.34',
        '10.42.42.42',
        '192.168.33.3'
    ]
)

atk_command = GremlinDiskSpaceAttack(
    blocksize=8,
    directory='/tmp',
    percent=100,
    workers=4
)

atk_helper = GremlinAttackHelper(
    target=atk_targets,
    command=atk_command
)

attacks.create_attack(body=atk_helper)
```

##### Disk IO



#### Stateful Attacks

##### Shutdown

##### Process Killer

##### Time Travel

#### Network Attacks

##### Blackhole

##### DNS

##### Latency

This will launch a 100ms latency attack, limited to ICMP traffic, against a single random container
with the ECS container-name `swissknife`

```python
from gremlinapi.config import GremlinAPIConfig as config
from gremlinapi.attacks import GremlinAPIAttacks as attacks

config.api_key = 'Key MU....ziTk....40z...c='
config.team_id = '9676868b-60d2-5ebe-aa66-c1de8162ff9d'

body = {
    'target': {
        'type': 'Random',
        'containers': {
            'multiSelectLabels': {
                "com.amazonaws.ecs.container-name": [
                    "swissknife"
                ]
            }
        },
        'exact': 1
    },
    'command': {
        'type': 'latency',
        'commandType': 'Latency',
        'args': [
            '-l', '60',
            '-h', '^api.gremlin.com',
            '-m', '100',
            '-P', 'ICMP'
        ],
        'providers': []
    }
}
attack_guid = attacks.create_attack(body=body, teamId=config.team_id)
```

##### Packet Loss

## List Attacks

```python
from gremlinapi.attacks import GremlinAPIAttacks as attacks
team_id = 'TEAM_ID/UUID'
attack_list = attacks.list_attacks(teamId=team_id)

from pprint import pprint
pprint(attack_list)
```

## List Active Attacks

```python
from gremlinapi.attacks import GremlinAPIAttacks as attacks
team_id = 'TEAM_ID/UUID'
active_attacks = attacks.list_active_attacks(teamId=team_id)

from pprint import pprint
pprint(active_attacks)
```

## List Completed Attacks

```python
from gremlinapi.attacks import GremlinAPIAttacks as attacks
team_id = 'TEAM_ID/UUID'
completed_attacks = attacks.list_completed_attacks(teamId=team_id)

from pprint import pprint
pprint(completed_attacks)
```

## Get Attack Details

```python
from gremlinapi.attacks import GremlinAPIAttacks as attacks
team_id = 'TEAM_ID/UUID'
attack_id = 'ATTACK_ID'
attack_details = attacks.get_attack(guid=attack_id, teamId=team_id)

from pprint import pprint
pprint(attack_details)
```

## Halt Attack

```python
from gremlinapi.attacks import GremlinAPIAttacks as attacks
team_id = 'TEAM_ID/UUID'
attack_id = 'ATTACK_ID'
confirmation = attacks.halt_attack(guid=attack_id, teamId=team_id)
```

## Halt _ALL_ Attacks

```python
from gremlinapi.attacks import GremlinAPIAttacks as attacks
team_id = 'TEAM_ID/UUID'

confirmation = attacks.halt_all_attacks(teamId=team_id)
```
