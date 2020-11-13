# Users

### List Users

```python
from gremlinapi.users import GremlinAPIUsers as users

team_id = 'Team ID/UUID'

user_list = users.list_users(teamId=team_id)
```

### Invite User
```python
from gremlinapi.users import GremlinAPIUsers as users

user_email = 'gizmo@gremlin.com'

confirmation = users.invite_user(email=user_email)
```

### Deactivate User
```python
from gremlinapi.users import GremlinAPIUsers as users
from gremlinapi.config import GremlinAPIConfig as config

config.bearer_token = 'BEARER TOKEN'
team_id = 'Team ID/UUID'
user_email = 'brain@gremlin.com'

confirmation = users.deactivate_user(email=user_email, teamId=team_id)
```

### Revoke Invite
```python
from gremlinapi.users import GremlinAPIUsers as users

user_email = 'mohawk@gremlin.com'

confirmation = users.revoke_user_invite(email=user_email)
```

