# gremlin-python

![](https://github.com/gremlin/gremlin-python/raw/master/Gremlin_Python_Icon.png?raw=true)

## Project Status
This is an unoffical PythonSDK currently in alpha testing. 

## Installation

### PyPi

```bash
pip3 install gremlinapi
```

### Install from source

```bash
git clone git@github.com:gremlin/gremlin-python.git
cd gremlin-python
python3 setup.py install
```

### Use Packaged Docker runtime

Build and run this project's self contained docker image with all the necessary dependencies
```shell script
  make docker-build && make docker-run-interactive
```

## Usage

### CLI

Coming soon

## Authenticate to the API

The Gremlin API requires a form of authentication, either API Key or Bearer Token. API Keys are the least privileged
form of authentication, are easy to manage and change, but do not allow for company wide actions 
[see https://www.gremlin.com/docs/api-reference/overview/](https://www.gremlin.com/docs/api-reference/overview/) for
a list of which API endpoints support API Keys vs. Bearer Tokens.

A bearer token may be provided to the API instead of an API Key, and this allow the owner of the bearer token to use
an escalated set of permissions and actions, pending the user has those roles in the RBAC schema. Because bearer tokens
are short lived, the user may chose to use the login function instead of directly providing a bearer token. The downside
to this is that user credentials are directly exposed, and may end up in logs. When using the login function, the Gremlin API will return a bearer token which will be used on the users behalf to
execute API actions.

#### Authentication Method Toggles

***Experimental - Improper use can lock you out of your account***

```python
toggles_body = {
    "companyId" : hooli_id,
    "passwordEnabled" : True,
    "mfaRequired" : False,
    "googleEnabled" : True,
    "oauthEnabled" : True,
    "samlEnabled" : True,
    "claimsRequired" : False,
}

GremlinAPIOAUTH.toggles(**toggles_body)
```

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

#### User Login

```python
import gremlinapi
gremlinapi.login(
    email='user@gremlin.com',
    password='looksL1keIshouldCh4ng3th1sagain!',
    company_name="Gremlin Inc."
)
```

#### User Login with MFA

```python
import gremlinapi
gremlinapi.login(
    email='user@gremlin.com',
    password='looksL1keIshouldCh4ng3th1sagain!',
    company_name="Gremlin Inc.",
    token="8675309"
)
```

#### Team IDs

When using a Gremlin RBAC enabled account, you must specify the `teamId` to parameter for most requests. Additionally,
you may supply this globally via the `GremlinAPIConfig` module:

```python
from gremlinapi.config import GremlinAPIConfig as config
config.team_id = team_id
```

### OAUTH

#### Authentication with OAUTH

To authentication through a desired OAUTH workflow, the required information is similar to `gremlinapi.login()`.

When successfully authenticated through OAUTH, the bearer token, used later in the API workflow, is returned.

```python
from gremlinapi.oauth import GremlinAPIOAUTH

GREMLIN_COMPANY = "Your Company Name"
USERNAME = "your.login.email@domain.com"
PASSWORD = "y0urPa$$w0rd"
OAUTH_LOGIN = "http://your.oauth.provider/login"

auth_args = {
    "email":USERNAME,
    "password": PASSWORD,
    "client_id": "mocklab_oauth2",
    "company_name": GREMLIN_COMPANY,
    "oauth_login_uri": OAUTH_LOGIN,
}

bearer_token = GremlinAPIOAUTH.authenticate(**auth_args)
```

#### OAUTH Configuration

OAUTH can be configured through an API endpoint per the following configuration dictionary and code example.

You must previous be logged in or otherwise authenticated for the below code to succeed.

```python
from gremlinapi.oauth import GremlinAPIOAUTH

GREMLIN_TEAM_ID = "your-team-id"

config_body = {
    # Used to authenticate against the OAuth provider. We will redirect the user to this URL when they initate a OAuth login.
    "authorizationUri": "http://your.oauth.provider/authorize",
    # Used to exchange an OAuth code, obtained after logging into the OAuth provider, for an access token.
    "tokenUri": "http://your.oauth.provider/oauth/token",
    # Used to query for the email of the user..
    "userInfoUri": "http://your.oauth.provider/userinfo",
    # The public identifier obtained when registering Gremlin with your OAuth provider.
    "clientId": "your_client_id",
    # The secret obtained when registering Gremlin with your OAuth provider.
    "clientSecret": "your_client_secret",
    # Define what level of access the access token will have that Gremlin obtains during the OAuth login. The default is `email`. If you change it from the default, the scope provided <strong>must</strong> be able to read the email of the user.
    "scope":"email",
}

GremlinAPIOAUTH.configure(GREMLIN_TEAM_ID, **config_body)
```

## Proxy Support

This library supports system wide `HTTP_PROXY` and `HTTPS_PROXY` environment variables.

Additionally, proxy configuration may be directly configured inside the library, or the use of 
`GREMLIN_HTTP_PROXY` and `GREMLIN_HTTPS_PROXY` can be utilized to isolate the communication stream.

### Direct Proxy Configuration

```python
from gremlinapi.config import GremlinAPIConfig as config
config.http_proxy = 'http://user:pass@myproxy:port'
config.https_proxy = 'https://user:pass@myproxy:port'
```

## Examples

See [Examples](examples/README.md) for more more functionality

### Launching Attacks

#### Example 1

This will launch a 100ms latency attack, limited to ICMP traffic, against a single random container
with the ECS container-name `swissknife`

```python
from gremlinapi.config import GremlinAPIConfig as config
from gremlinapi.attacks import GremlinAPIAttacks as attacks
config.bearer_token = 'Bearer MU....ziTk....40z...c='
config.team_id = 'e7352a6b-a9a0-513c-81e4-980f680a70c4'
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

### Organization and Team management

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

```javascript
[
    {
        'active': True,
        'auto_add_users': False,
        'certificate_expiration_imminent': False,
        'certificate_expires_on': '2021-02-02T18:38:54.000Z',
        'certificate_set_at': '2020-02-03T18:38:54.654Z',
        'certificate_set_by': 'community@gremlin.com',
        'company_id': '07814fbb-a9a0-81e4-b375-980f680a70c4',
        'created_at': '2020-02-03T18:38:54.654Z',
        'identifier': 'cb7ca0d3-4bac-542c-9059-3ee48df857fa',
        'idle': False,
        'name': 'testteam1',
        'secret_set_at': '2020-02-03T18:38:54.654Z',
        'secret_set_by': 'community@gremlin.com',
        'updated_at': '2020-02-03T18:38:54.654Z'
    },
    {
        'active': True,
        'auto_add_users': False,
        'certificate_expiration_imminent': False,
        'certificate_expires_on': '2021-02-02T18:40:33.000Z',
        'certificate_set_at': '2020-02-03T18:40:33.967Z',
        'certificate_set_by': 'community@gremlin.com',
        'company_id': '07814fbb-a9a0-81e4-b375-980f680a70c4',
        'created_at': '2020-02-03T18:40:33.967Z',
        'identifier': 'c049bf49-f236-5df7-9e2e-5c3858e32426',
        'idle': False,
        'name': 'testteam2',
        'secret_set_at': '2020-02-03T18:40:33.967Z',
        'secret_set_by': 'community@gremlin.com',
        'updated_at': '2020-02-03T18:40:33.967Z'
    },
    {
        'active': True,
        'auto_add_users': False,
        'certificate_expiration_imminent': False,
        'certificate_expires_on': '2021-03-19T18:03:54.000Z',
        'certificate_set_at': '2020-03-19T18:03:54.355Z',
        'certificate_set_by': 'community@gremlin.com',
        'company_id': '07814fbb-a9a0-81e4-b375-980f680a70c4',
        'created_at': '2020-03-19T18:03:54.355Z',
        'identifier': 'df51deb3-3fa6-5e9e-947f-9d5ef62418f1',
        'idle': False,
        'name': 'My New Awesome Team Name',
        'updated_at': '2020-03-19T18:03:54.355Z'
    }
]
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

```javascript
{
    'has_secret': True,
    'org_id': 'e7352a6b-a9a0-513c-81e4-980f680a70c4',
    'pem_encoded_certificate': '-----BEGIN CERTIFICATE-----\nMIIBvDCCA ....=\n-----END CERTIFICATE-----\n',
    'pem_encoded_private_key': '-----BEGIN EC PRIVATE KEY-----\nMHcCAQEE ....\n-----END EC PRIVATE KEY-----\n'
}
```

### Scenarios

#### List all scenarios

```python
from gremlinapi.config import GremlinAPIConfig as config
from gremlinapi.scenarios import GremlinAPIScenarios as scenarios
config.bearer_token = 'Bearer MU3...ZiTk...Lo...4zO..c='
team_id = 'e7352a6b-a9a0-513c-81e4-980f680a70c4'
scenarios_list = scenarios.list_scenarios(teamId=team_id)
```

```python
import pprint
pprint.pprint(scenarios_list)
```

```javascript
[
    {
        'create_source': 'WebApp',
        'created_at': '2019-10-14T21:02:47.397Z',
        'created_by': 'community@gremlin.com',
        'description': 'Confidently adopt cloud auto-scaling services. Verify your '
        'users have a positive experience and your application '
        'behaves as expected while hosts come and go.',
        'guid': 'ed49ebae-d45d-4412-89eb-aed45d841255',
        'hypothesis': 'When CPU usage ramps up and hits a set threshold, active '
        'instances will increase and decrease when CPU usage goes '
        'down. User sessions will remain active without throwing any '
        'errors.',
        'last_run_at': '2019-10-14T21:02:47.865Z',
        'name': 'Validate Auto-Scaling',
        'org_id': 'e7352a6b-a9a0-513c-81e4-980f680a70c4',
        'recommended_scenario_id': 'd543fb53-cbd8-4b92-83fb-53cbd8cb9250',
        'state': 'PUBLISHED',
        'steps': [{
                'attacks': [{
                    'attackType': 'ILFI',
                    'impactDefinition': {
                        'commandArgs': {
                            'allCores': True,
                            'cliArgs': ['cpu',
                                '-l',
                                '60',
                                '-p',
                                '5',
                                '-a'
                            ],
                            'length': 60,
                            'percent': 5
                        },
                        'commandType': 'CPU'
                    },
                    'targetDefinition': {
                        'strategy': {
                            'percentage': 100
                        },
                        'strategyType': 'Random',
                        'targetType': 'Container'
                    }
                }],
                'delay': 5
            },
            {
                'attacks': [{
                    'attackType': 'ILFI',
                    'impactDefinition': {
                        'commandArgs': {
                            'allCores': True,
                            'cliArgs': ['cpu',
                                '-l',
                                '60',
                                '-p',
                                '10',
                                '-a'
                            ],
                            'length': 60,
                            'percent': 10
                        },
                        'commandType': 'CPU'
                    },
                    'targetDefinition': {
                        'strategy': {
                            'percentage': 100
                        },
                        'strategyType': 'Random',
                        'targetType': 'Container'
                    }
                }],
                'delay': 5
            },
            {
                'attacks': [{
                    'attackType': 'ILFI',
                    'impactDefinition': {
                        'commandArgs': {
                            'allCores': True,
                            'cliArgs': ['cpu',
                                '-l',
                                '60',
                                '-p',
                                '15',
                                '-a'
                            ],
                            'length': 60,
                            'percent': 15
                        },
                        'commandType': 'CPU'
                    },
                    'targetDefinition': {
                        'strategy': {
                            'percentage': 100
                        },
                        'strategyType': 'Random',
                        'targetType': 'Container'
                    }
                }],
                'delay': 5
            },
            {
                'attacks': [{
                    'attackType': 'ILFI',
                    'impactDefinition': {
                        'commandArgs': {
                            'allCores': True,
                            'cliArgs': ['cpu',
                                '-l',
                                '60',
                                '-p',
                                '20',
                                '-a'
                            ],
                            'length': 60,
                            'percent': 20
                        },
                        'commandType': 'CPU'
                    },
                    'targetDefinition': {
                        'strategy': {
                            'percentage': 100
                        },
                        'strategyType': 'Random',
                        'targetType': 'Container'
                    }
                }],
                'delay': 5
            }
        ],
        'tiers': ['Free', 'Enterprise'],
        'updated_at': '2019-10-14T21:02:48.107Z'
    },
    {
        'create_source': 'WebApp',
        'created_at': '2019-10-14T20:36:59.952Z',
        'created_by': 'community@gremlin.com',
        'description': 'Confidently adopt cloud auto-scaling services. Verify your '
        'users have a positive experience and your application '
        'behaves as expected while hosts come and go.',
        'guid': 'bdaeef1c-4dbd-47bd-aeef-1c4dbdf7bd3a',
        'hypothesis': 'When CPU usage ramps up and hits a set threshold, active '
        'instances will increase and decrease when CPU usage goes '
        'down. User sessions will remain active without throwing any '
        'errors.',
        'last_run_at': '2019-10-14T20:37:00.128Z',
        'name': 'Validate Auto-Scaling',
        'org_id': 'e7352a6b-a9a0-513c-81e4-980f680a70c4',
        'recommended_scenario_id': 'd543fb53-cbd8-4b92-83fb-53cbd8cb9250',
        'state': 'PUBLISHED',
        'steps': [{
                'attacks': [{
                    'attackType': 'ILFI',
                    'impactDefinition': {
                        'commandArgs': {
                            'allCores': True,
                            'cliArgs': ['cpu',
                                '-l',
                                '60',
                                '-p',
                                '5',
                                '-a'
                            ],
                            'length': 60,
                            'percent': 5
                        },
                        'commandType': 'CPU'
                    },
                    'targetDefinition': {
                        'strategy': {
                            'percentage': 100
                        },
                        'strategyType': 'Random',
                        'targetType': 'Container'
                    }
                }],
                'delay': 5
            },
            {
                'attacks': [{
                    'attackType': 'ILFI',
                    'impactDefinition': {
                        'commandArgs': {
                            'allCores': True,
                            'cliArgs': ['cpu',
                                '-l',
                                '60',
                                '-p',
                                '10',
                                '-a'
                            ],
                            'length': 60,
                            'percent': 10
                        },
                        'commandType': 'CPU'
                    },
                    'targetDefinition': {
                        'strategy': {
                            'percentage': 100
                        },
                        'strategyType': 'Random',
                        'targetType': 'Container'
                    }
                }],
                'delay': 5
            },
            {
                'attacks': [{
                    'attackType': 'ILFI',
                    'impactDefinition': {
                        'commandArgs': {
                            'allCores': True,
                            'cliArgs': ['cpu',
                                '-l',
                                '60',
                                '-p',
                                '15',
                                '-a'
                            ],
                            'length': 60,
                            'percent': 15
                        },
                        'commandType': 'CPU'
                    },
                    'targetDefinition': {
                        'strategy': {
                            'percentage': 100
                        },
                        'strategyType': 'Random',
                        'targetType': 'Container'
                    }
                }],
                'delay': 5
            },
            {
                'attacks': [{
                    'attackType': 'ILFI',
                    'impactDefinition': {
                        'commandArgs': {
                            'allCores': True,
                            'cliArgs': ['cpu',
                                '-l',
                                '60',
                                '-p',
                                '20',
                                '-a'
                            ],
                            'length': 60,
                            'percent': 20
                        },
                        'commandType': 'CPU'
                    },
                    'targetDefinition': {
                        'strategy': {
                            'percentage': 100
                        },
                        'strategyType': 'Random',
                        'targetType': 'Container'
                    }
                }],
                'delay': 5
            }
        ],
        'tiers': ['Free', 'Enterprise'],
        'updated_at': '2019-10-14T20:37:00.314Z'
    },
    ....
]
```

#### Create scenario
```python
from gremlinapi.config import GremlinAPIConfig as config
from gremlinapi.attack_helpers import (
    GremlinBlackholeAttack,
    GremlinTargetContainers,
)
from gremlinapi.scenarios import GremlinAPIScenarios as scenarios
from gremlinapi.scenario_graph_helpers import (
    GremlinScenarioGraphHelper,
    GremlinScenarioILFINode,
    GremlinScenarioDelayNode
)
# config.bearer_token = 'Bearer MU3...ZiTk...Lo...4zO..c='
config.api_key = "" #TODO: populate
config.team_id = "" #TODO: populate

blast_radius = 100
delay_time = 5

#create scenario
new_scenario = GremlinScenarioGraphHelper(
    name="A Code-Created Scenario",
    description="Python SDK created scenario",
    hypothesis="No Hypothesis",
)

#create scenario nodes
black_hole_node_1 = GremlinScenarioILFINode(
    command=GremlinBlackholeAttack(),
    target=GremlinTargetContainers(
        strategy_type="Random", labels={"owner": "kyle"}, percent=blast_radius
    ),
)
delay_node_1 = GremlinScenarioDelayNode(description="Add some delay", delay=delay_time)
black_hole_node_2 = GremlinScenarioILFINode(
    command=GremlinBlackholeAttack(),
    target=GremlinTargetContainers(
        strategy_type="Random", labels={"owner": "kyle"}, percent=blast_radius
    ),
)

#add scenario nodes
new_scenario.add_node(black_hole_node_1)
new_scenario.add_node(black_hole_node_2)
new_scenario.add_node(delay_node_1)

#add node edges
new_scenario.add_edge(black_hole_node_1, delay_node_1)
new_scenario.add_edge(delay_node_1, black_hole_node_2)

#submit scenario to api
scenarios.create_scenario(body=new_scenario)
```

## Support

Support for this library is provided by the Chaos Engineering community.
[Join us on slack!](https://www.gremlin.com/slack/)
