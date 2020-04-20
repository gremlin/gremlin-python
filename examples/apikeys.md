# apikeys endpoint


#### Create API Key

Since your creating an API keys, it's likely you don't have an existing one use. Using environment variables is an easy
way to provide authentication to the library.
```bash
#!/bin/bash
export GREMLIN_USER=my-gremlin-username
export GREMLIN_PASSWORD=my-gremlin-password
export GREMLIN_TEAM_ID=my-gremlin-teamid
```

And the python to create the api-key:
```python
import gremlinapi
from gremlinapi.apikeys import GremlinAPIapikeys as apikeys

gremlinapi.login()
key_string = apikeys.create_apikey(identifier='my-first-apikey', description='This is our first API key')
print(f'Set the environment variable GREMLIN_API_KEY to {key_string}')
```


#### List API Keys

```python
from gremlinapi.apikeys import GremlinAPIapikeys as apikeys
from pprint import pprint
keys = apikeys.list_apikeys()
pprint(keys)
```

#### Revoke API Keys

```python
from gremlinapi.apikeys import GremlinAPIapikeys as apikeys
from pprint import pprint
resp = apikeys.revoke_apikey(identifier='my-api-key-identifier')
pprint(resp)
```