# Attacks

## Create Attacks

### Attack Examples

#### Resource Attacks

##### CPU

##### Memory

##### Disk IO

##### Disk Space

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
