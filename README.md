# gremlin-python

## Installation

python3 setup.py install

## Usage

## Authentication

#### API User Keys

```python
from gremlinapi.config import GremlinAPIConfig as config
config.api_key = 'Key MU3...ZiTk...Lo...4zO..c='
```

#### User Provided Bearer Token

```python
from gremlinapi.config import GremlinAPIConfig as config
config.bearer_token = 'Bearer MU3...ZiTk...Lo...4zO..c='
```

#### User login

```python
import gremlinapi
gremlinapi.login(email='kyle@gremlin.com',
                 password='looksL1keIshouldCh4ng3th1sagain!',
                 company_name="Gremlin Inc.")
```

```python
import gremlinapi
gremlinapi.login(email='kyle@gremlin.com',
                 password='looksL1keIshouldCh4ng3th1sagain!',
                 company_name="Gremlin Inc.",
                 token="8675309")

```

## Launching Attacks

#### Example 1

This will launch a 100ms latency attack, limited to ICMP traffic, against a single random container
with the ECS container-name `swissknife`

```python
from gremlinapi.config import GremlinAPIConfig as config
from gremlinapi.attacks import GremlinAPIAttacks as attacks
config.bearer_token = 'Bearer MU....ziTk....40z...c='
config.team_guid = '9676868b-60d2-5ebe-aa66-c1de8162ff9d'
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
attacks.create_attack(body=body, teamId=config.team_guid)
```

## Organization and Team management

```python
import gremlinapi
gremlinapi.config.GremlinAPIConfig.bearer_token = 'Bearer MU3...ZiTk...Lo...4zO..c='
gremlinapi.orgs.GremlinAPIOrgs.list_orgs()
```