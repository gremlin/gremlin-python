# Schedules


### List active schedules
```python
from gremlinapi.schedules import GremlinAPISchedules as schedules

schedule_list = schedules.list_active_schedules()
```

### List attack schedules
```python
from gremlinapi.schedules import GremlinAPISchedules as schedules

schedule_list = schedules.list_attack_schedules()
```

### List Scenario schedules
```python
from gremlinapi.schedules import GremlinAPISchedules as schedules

schedule_list = schedules.list_scenario_schedules()
```


### Create Attack Schedule
```python
from gremlinapi.schedules import GremlinAPISchedules as schedules

team_id = 'TEAM ID/UUID'

schedule_body = {
    'command': {
        'type': 'cpu',
        'args': ['-l', '60', '-c', '1']
    },
    'target': {
        'exact': 1,
        'type': 'Random'
    },
    'trigger': {
        'activeDays': ['M', 'T', 'W', 'Th', 'F'],
        'start': '23:00',
        'end': '23:30',
        'timeZone': 'America/New_York',
        'type': 'Random',
        'maxRuns': 1
    }
}

confirmation = schedules.create_attack_schedule(body=schedule_body, teamId=team_id)
```