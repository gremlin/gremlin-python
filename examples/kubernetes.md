# Kubernetes

### List All Kubernetes Attacks
```python
from gremlinapi.kubernetes import GremlinAPIKubernetesAttacks as k8attacks
team_id = 'TEAM_ID/UUID'

attack_list = k8attacks.list_all_kubernetes_attacks(teamId=team_id)
```

### Get attack details
```python
from gremlinapi.kubernetes import GremlinAPIKubernetesAttacks as k8attacks
team_id = 'TEAM_ID/UUID'
attack_id = 'ATTACK_UID'

attack_details = k8attacks.get_kubernetes_attack(uid=attack_id, teamId=team_id)
```

### Halt Kubernetes Attack
```python
from gremlinapi.kubernetes import GremlinAPIKubernetesAttacks as k8attacks
team_id = 'TEAM_ID/UUID'
attack_id = 'ATTACK_ID'

confirmation = k8attacks.halt_kubernetes_attack(uid=attack_id, teamId=team_id)
```

### Halt All Kubernetes Attacks
```python
from gremlinapi.kubernetes import GremlinAPIKubernetesAttacks as k8attacks
team_id = 'TEAM_ID/UUID'

confirmation = k8attacks.halt_all_kubernetes_attacks(teamId=team_id)
```