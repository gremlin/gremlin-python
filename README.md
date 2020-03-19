# gremlin-python

## Installation

python3 setup.py install

## Usage

## Basic Authentication

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
attack_guid = attacks.create_attack(body=body, teamId=config.team_guid)
```

## Organization and Team management

#### List all teams
```python
from gremlinapi.config import GremlinAPIConfig as config
from gremlinapi.orgs import GremlinAPIOrgs as orgs
config.bearer_token = 'Bearer MU3...ZiTk...Lo...4zO..c='
all_orgs = orgs.list_orgs()
```

```python
import pprint
pprint.pprint(all_orgs)
```

```python
[{'active': True,
  'auto_add_users': False,
  'certificate_expiration_imminent': False,
  'certificate_expires_on': '2021-02-02T18:38:54.000Z',
  'certificate_set_at': '2020-02-03T18:38:54.654Z',
  'certificate_set_by': 'john+demo@gremlin.com',
  'company_id': '9676868b-60d2-5ebe-aa66-c1de8162ff9d',
  'created_at': '2020-02-03T18:38:54.654Z',
  'identifier': 'cb7ca0d3-4bac-542c-9059-3ee48df857fa',
  'idle': False,
  'name': 'testteam1',
  'secret_set_at': '2020-02-03T18:38:54.654Z',
  'secret_set_by': 'john+demo@gremlin.com',
  'updated_at': '2020-02-03T18:38:54.654Z'},
 {'active': True,
  'auto_add_users': False,
  'certificate_expiration_imminent': False,
  'certificate_expires_on': '2021-02-02T18:40:33.000Z',
  'certificate_set_at': '2020-02-03T18:40:33.967Z',
  'certificate_set_by': 'john+demo@gremlin.com',
  'company_id': '9676868b-60d2-5ebe-aa66-c1de8162ff9d',
  'created_at': '2020-02-03T18:40:33.967Z',
  'identifier': 'c049bf49-f236-5df7-9e2e-5c3858e32426',
  'idle': False,
  'name': 'testteam2',
  'secret_set_at': '2020-02-03T18:40:33.967Z',
  'secret_set_by': 'john+demo@gremlin.com',
  'updated_at': '2020-02-03T18:40:33.967Z'},
 {'active': True,
  'auto_add_users': False,
  'certificate_expiration_imminent': False,
  'certificate_expires_on': '2021-03-19T18:03:54.000Z',
  'certificate_set_at': '2020-03-19T18:03:54.355Z',
  'certificate_set_by': 'kyle+demo@gremlin.com',
  'company_id': '9676868b-60d2-5ebe-aa66-c1de8162ff9d',
  'created_at': '2020-03-19T18:03:54.355Z',
  'identifier': 'df51deb3-3fa6-5e9e-947f-9d5ef62418f1',
  'idle': False,
  'name': 'My New Awesome Team Name',
  'updated_at': '2020-03-19T18:03:54.355Z'}]
```

#### Create a team
```python
from gremlinapi.config import GremlinAPIConfig as config
from gremlinapi.orgs import GremlinAPIOrgs as orgs
config.bearer_token = 'Bearer MU3...ZiTk...Lo...4zO..c='
new_team_details = orgs.create_org(name='My New Awesome Team Name')
```

```python
import pprint
pprint.pprint(new_team_details)
```

```python
{'has_secret': True,
 'org_id': 'df51deb3-3fa6-5e9e-947f-9d5ef62418f1',
 'pem_encoded_certificate': '-----BEGIN CERTIFICATE-----\n'
                            'MIIBvDCCAWKgAwIBAgIBATAKBggqhkjOPQQDAjBYMSMwIQYDVQQDDBpHcmVtbGlu\n'
                            'IENsaWVudCBDZXJ0aWZpY2F0ZTEOMAwGA1UECwwFSG9vbGkxITAfBgNVBAoMGE15\n'
                            'IE5ldyBBd2Vzb21lIFRlYW0gTmFtZTAeFw0yMDAzMTkxODAzNTRaFw0yMTAzMTkx\n'
                            'ODAzNTRaMFgxIzAhBgNVBAMMGkdyZW1saW4gQ2xpZW50IENlcnRpZmljYXRlMQ4w\n'
                            'DAYDVQQLDAVIb29saTEhMB8GA1UECgwYTXkgTmV3IEF3ZXNvbWUgVGVhbSBOYW1l\n'
                            'MFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEOEb1Dxa58N95g30S9S05B0v3O9US\n'
                            'Ug1hAuxKfxjLHeuO/R60yuR5RYZ0y4lz87iUSI4eAaBGhCLkwba4GyvZqKMdMBsw\n'
                            'CQYDVR0TBAIwADAOBgNVHQ8BAf8EBAMCB4AwCgYIKoZIzj0EAwIDSAAwRQIhAJiG\n'
                            'g6MA9ortNvkWGzhTa02SA15G31hcSKVrQXbCgwrOAiBVgaCFsrZxq5Vg+EUvevwQ\n'
                            'v8470+Rt7YEGxpn3GDCI6Q==\n'
                            '-----END CERTIFICATE-----\n',
 'pem_encoded_private_key': '-----BEGIN EC PRIVATE KEY-----\n'
                            'MHcCAQEEILujxbpH0qAtcjZTmutPWvWgbWwa9VseQqFH/aJE1BntoAoGCCqGSM49\n'
                            'AwEHoUQDQgAEOEb1Dxa58N95g30S9S05B0v3O9USUg1hAuxKfxjLHeuO/R60yuR5\n'
                            'RYZ0y4lz87iUSI4eAaBGhCLkwba4GyvZqA==\n'
                            '-----END EC PRIVATE KEY-----\n'}

```