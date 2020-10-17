from calm.dsl.builtins import Deployment, ref

from packages import DemoAppPackage, HaproxyPackage, PostgresPackage
from substrates import DemoAppVMS, HaproxyVMS, PostgresEraSubstrate


class DemoAppAhvDeployment(Deployment):

    min_replicas = '1'
    max_replicas = '1'

    packages = [ref(DemoAppPackage)]
    substrate = ref(DemoAppVMS)


class HaproxyAhvDeployment(Deployment):
    min_replicas = '1'
    max_replicas = '1'

    packages = [ref(HaproxyPackage)]
    substrate = ref(HaproxyVMS)


class PostgresHAonEraDeployment(Deployment):
    min_replicas = '1'
    max_replicas = '1'
    default_replicas = '1'

    packages = [ref(PostgresPackage)]
    substrate = ref(PostgresEraSubstrate)
