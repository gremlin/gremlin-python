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

### Attack 50% of a Kubernetes Deployment
```python
from gremlinapi.kubernetes import GremlinAPIKubernetesAttacks as k8s_attacks
from kubernetes_attack_helpers import GremlinKubernetesAttackTarget, GremlinKubernetesAttackTargetHelper, GremlinKubernetesAttackHelper
from gremlinapi.attack_helpers import GremlinBlackholeAttack

config.api_key = <API_KEY>
config.team_id = <TEAM_ID>

k8s_attacks.new_kubernetes_attack(
    body = GremlinKubernetesAttackHelper(
        command = GremlinBlackholeAttack(),
        target = GremlinKubernetesAttackTargetHelper(
            targets = [
                GremlinKubernetesAttackTarget(
                    cluster_id = "<CLUSTER_ID>",
                    namespace = "<NAMESPACE>",
                    kind = "DEPLOYMENT",
                    name = "<deployment_name>
                )
            ],
            percentage = 50
        )
    )
)
```

### Attack 3 pods of a Kubernetes ReplicaSet
```python
from gremlinapi.kubernetes import GremlinAPIKubernetesAttacks as k8s_attacks
from kubernetes_attack_helpers import GremlinKubernetesAttackTarget, GremlinKubernetesAttackTargetHelper, GremlinKubernetesAttackHelper
from gremlinapi.attack_helpers import GremlinBlackholeAttack

config.api_key = <API_KEY>
config.team_id = <TEAM_ID>

k8s_attacks.new_kubernetes_attack(
    body = GremlinKubernetesAttackHelper(
        command = GremlinBlackholeAttack(),
        target = GremlinKubernetesAttackTargetHelper(
            targets = [
                GremlinKubernetesAttackTarget(
                    cluster_id = "<CLUSTER_ID>",
                    namespace = "<NAMESPACE>",
                    kind = "REPLICASET",
                    name = "<deployment_name>
                )
            ],
            count = 3
        )
    )
)
```