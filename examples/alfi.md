# Alfi Examples

### Create ALFI Experiments

Coming Soon

### Get ALFI Experiment Details

```python
from gremlinapi.alfi import GremlinALFI as alfi
from pprint import pprint

alfi_attack_id = 'expirment-guid'
experiment_details = alfi.get_alfi_experiment_details(guid=alfi_attack_id)

pprint(experiment_details)
```

### Halt ALFI Experiment

```python
from gremlinapi.alfi import GremlinALFI as alfi

alfi_attack_id = 'expirment-guid'
alfi.halt_alfi_experiment(guid=alfi_attack_id)
```

### Halt _ALL_ ALFI Experiments

```python
from gremlinapi.alfi import GremlinALFI as alfi

alfi.halt_all_alfi_experiments()
```

### List Active ALFI Experiments

```python
from gremlinapi.alfi import GremlinALFI as alfi
from pprint import pprint

experiment_list = alfi.list_active_alfi_experiments()

pprint(experiment_list)
```

### List Completed ALFI Experiments

```python
from gremlinapi.alfi import GremlinALFI as alfi
from pprint import pprint

experiment_list = alfi.list_completed_alfi_experiments()

pprint(experiment_list)
```
