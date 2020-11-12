from calm.dsl.builtins import Deployment, ref

from packages import MssqlPackage
from substrates import MssqlEraSubstrate


class PostgresHAonEraDeployment(Deployment):
    min_replicas = '1'
    max_replicas = '1'
    default_replicas = '1'

    packages = [ref(MssqlPackage)]
    substrate = ref(MssqlEraSubstrate)
