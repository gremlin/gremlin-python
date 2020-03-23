# Clients Endpoint Examples

### Activate Client

```python
from gremlinapi.clients import GremlinAPIClients as clients
team_id = 'TEAM_ID'
client_guid = 'CLIENT_GUID'

response = clients.activate_client(guid=client_guid, teamId=team_id)
```

### Deactivate Client

```python
from gremlinapi.clients import GremlinAPIClients as clients
team_id = 'TEAM_ID'
client_guid = 'CLIENT_GUID'

response = clients.deactivate_client(guid=client_guid, teamId=team_id)
```

### List Clients

```python
from gremlinapi.clients import GremlinAPIClients as clients
team_id = 'TEAM_ID'

client_list = clients.list_clients(teamId=team_id)
```

### List Active Clients

```python
from gremlinapi.clients import GremlinAPIClients as clients
team_id = 'TEAM_ID'

client_list = clients.list_active_clients(teamId=team_id)
```
