# Organizations

### Create Team
```python
from gremlinapi.orgs import GremlinAPIOrgs as orgs
from gremlinapi.config import GremlinAPIConfig as config

config.bearer_token = 'BEARER_TOKEN'

new_team_name = 'Mohawks_Gremlins'
details = orgs.create_org(name=new_team_name)
```

### List Teams
```python
from gremlinapi.orgs import GremlinAPIOrgs as orgs

org_list = orgs.list_orgs()
```

### Get Team Details
```python
from gremlinapi.orgs import GremlinAPIOrgs as orgs

team_id = 'TEAM ID/UUID'

team_details = orgs.get_org(identifier=team_id)
```

### Create New Certificates for Team Agents
```python
from gremlinapi.orgs import GremlinAPIOrgs as orgs
from gremlinapi.config import GremlinAPIConfig as config

config.bearer_token = 'BEARER_TOKEN'
team_id = 'TEAM ID/UUID'

new_certs = orgs.new_certificate(teamId=team_id)
```