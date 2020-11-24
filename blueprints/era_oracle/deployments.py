from calm.dsl.builtins import Deployment, ref

from packages import OraclePackage
from substrates import OracleEraSubstrate


class OracleOnEraDeployment(Deployment):
    min_replicas = '1'
    max_replicas = '1'
    default_replicas = '1'

    packages = [ref(OraclePackage)]
    substrate = ref(OracleEraSubstrate)
