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

## Organization and Team management

```python
import gremlinapi
gremlinapi.config.GremlinAPIConfig.bearer_token = 'Bearer MU3...ZiTk...Lo...4zO..c='
gremlinapi.orgs.GremlinAPIOrgs.list_orgs()
```