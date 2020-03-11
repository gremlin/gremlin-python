# gremlin-python

## Installation

## Usage

## Authentication

#### API User Keys

#### User Provided Bearer Token

#### User login

```python
import gremlinapi as gapi

gapi.login(user=user, password=password)

```

## Launching Attacks

## Organization and Team management

```python
import gremlinapi
gremlinapi.config.GremlinAPIConfig.bearer_token = 'Bearer MU3...ZiTk...Lo...4zO..c='
gremlinapi.orgs.GremlinAPIOrgs.list_orgs()
```