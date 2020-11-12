from calm.dsl.builtins import Deployment, ref

from packages import PostgresPackage
from substrates import PostgresEraSubstrate


class PostgresHAonEraDeployment(Deployment):
    min_replicas = '1'
    max_replicas = '1'
    default_replicas = '1'

    packages = [ref(PostgresPackage)]
    substrate = ref(PostgresEraSubstrate)
