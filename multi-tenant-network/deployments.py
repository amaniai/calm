from calm.dsl.builtins import Deployment, ref

from packages import AristaPackage
from substrates import AristaSubstrate


class AristaDeployment(Deployment):
    min_replicas = '1'
    max_replicas = '1'
    default_replicas = '1'

    packages = [ref(AristaPackage)]
    substrate = ref(AristaSubstrate)
