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
        target=GremlinTargetContainers(strategy_type='Random', labels={'owner': 'kyle'}, percent=100),
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

```python
from gremlinapi.attacks import GremlinAPIAttacks as attacks
from gremlinapi.attack_helpers import GremlinAttackHelper, GremlinTargetHosts, GremlinDiskIOAttack

atk_targets = GremlinTargetHosts(
    type='Exact',
    ids=[
        '10.189.7.34',
        '10.42.42.42',
        '192.168.33.3'
    ]
)

atk_command = GremlinDiskIOAttack(
    blockcount=8,
    blocksize=8,
    directory='/tmp',
    mode='rw',
    workers=8
)

atk_helper = GremlinAttackHelper(
    target=atk_targets,
    command=atk_command
)

attacks.create_attack(body=atk_helper)
```

#### Stateful Attacks

##### Shutdown

Wait one minutes, then shutdown 10% of containers tagged with app=webserver
```python
from gremlinapi.attacks import GremlinAPIAttacks as attacks
from gremlinapi.attack_helpers import GremlinAttackHelper, GremlinTargetContainers, GremlinShutdownAttack

attacks.create_attack(
    body=GremlinAttackHelper(
        target=GremlinTargetContainers(strategy_type='Random', labels={'app': 'webapp'}, percent=10),
        command=GremlinShutdownAttack(delay=1)))
```


Wait one minutes, then reboot 10% of hosts tagged with function=k8worker
```python
from gremlinapi.attacks import GremlinAPIAttacks as attacks
from gremlinapi.attack_helpers import GremlinAttackHelper, GremlinTargetHosts, GremlinShutdownAttack

attacks.create_attack(
    body=GremlinAttackHelper(
        target=GremlinTargetHosts(strategy_type='Random', tags={'function': 'k8worker'}, percent=10),
        command=GremlinShutdownAttack(delay=1, reboot=True)))
```

##### Process Killer

Kill httpd process using full-match posix regular expression on 10 percent of hosts tagged with role=webserver
```python
from gremlinapi.attacks import GremlinAPIAttacks as attacks
from gremlinapi.attack_helpers import GremlinAttackHelper, GremlinTargetHosts, GremlinProcessKillerAttack

attacks.create_attack(
    body=GremlinAttackHelper(
        target=GremlinTargetHosts(strategy_type='Random', tags={'role': 'webserver'}, percent=10),
        command=GremlinProcessKillerAttack(process='httpd', full_match=True)))
```

##### Time Travel

Time travel a single random host one year into the future, disabling NTP
```python
from gremlinapi.attacks import GremlinAPIAttacks as attacks
from gremlinapi.attack_helpers import GremlinAttackHelper, GremlinTargetHosts, GremlinTimeTravelAttack

attacks.create_attack(
    body=GremlinAttackHelper(
        target=GremlinTargetHosts(strategy_type='Random', target_all_hosts=True, exact=1),
        command=GremlinTimeTravelAttack(offset=365*3600*24, block_ntp=True)))
```

#### Network Attacks

##### Blackhole

Blackhole all traffic for exactly one random host
```python
from gremlinapi.attacks import GremlinAPIAttacks as attacks
from gremlinapi.attack_helpers import GremlinAttackHelper, GremlinTargetHosts, GremlinBlackholeAttack

attacks.create_attack(
    body=GremlinAttackHelper(
        target=GremlinTargetHosts(strategy_type='Random', target_all_hosts=True, exact=1),
        command=GremlinBlackholeAttack()))
```

##### DNS

Block lookups to [Google's DNS service](https://developers.google.com/speed/public-dns) for one lucky host
```python
from gremlinapi.attacks import GremlinAPIAttacks as attacks
from gremlinapi.attack_helpers import GremlinAttackHelper, GremlinTargetHosts, GremlinDNSAttack

attacks.create_attack(
    body=GremlinAttackHelper(
        target=GremlinTargetHosts(strategy_type='Random', target_all_hosts=True, exact=1),
        command=GremlinDNSAttack(ips=['8.8.8.8', '8.8.4.4'])))
```

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
        ]
    }
}
attack_guid = attacks.create_attack(body=body, teamId=config.team_id)
```

This will also launch a 100ms latency attack, limited to ICMP traffic, against a single random container
with the ECS container-name `swissknife`, using the built in helper vs. providing your own json

```python
from gremlinapi.attacks import GremlinAPIAttacks as attacks
from gremlinapi.attack_helpers import GremlinAttackHelper, GremlinTargetContainers, GremlinLatencyAttack

attacks.create_attack(
    body=GremlinAttackHelper(
        target=GremlinTargetContainers(strategy_type='Random', target_all_hosts=True,
            percent=100, labels={'com.amazonaws.ecs.container-start': 'swissknife'}),
        command=GremlinLatencyAttack(length=300, protocol='ICMP', delay=100)))
```

##### Packet Loss

This will use the packet corruption feature of packet loss to disrupt 10% of the traffic on 10% of the containers
```python
from gremlinapi.attacks import GremlinAPIAttacks as attacks
from gremlinapi.attack_helpers import GremlinAttackHelper, GremlinTargetContainers, GremlinPacketLossAttack

attacks.create_attack(
    body=GremlinAttackHelper(
        target=GremlinTargetContainers(strategy_type='Random', target_all_containers=True, percent=10),
        command=GremlinPacketLossAttack(corrupt=True, percent=10)))
```

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
