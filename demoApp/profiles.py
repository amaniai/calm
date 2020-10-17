from calm.dsl.builtins import Profile, CalmVariable

from deployments import DemoAppAhvDeployment, HaproxyAhvDeployment, PostgresHAonEraDeployment
from vars import DB_PASSWORD_VALUE


class Production(Profile):

    deployments = [DemoAppAhvDeployment, HaproxyAhvDeployment, PostgresHAonEraDeployment]

    DB_PASSWORD = CalmVariable.Simple(DB_PASSWORD_VALUE, label='DB Password', is_mandatory=True, runtime=True)
    ERA_IP = CalmVariable.Simple('10.38.11.10', label='ERA IP', is_mandatory=True, runtime=True)
    DBSERVER_NAME = CalmVariable.Simple('DB1', label='DB Server Name', is_mandatory=True, runtime=True)
    DB_NAME = CalmVariable.Simple('app', label='DB Name', is_mandatory=True, runtime=True)

    # hidden parameters
    COMPUTE_PROFILE = CalmVariable.Simple('DEFAULT_OOB_COMPUTE', is_hidden=True, runtime=False)
    DATABASE_PARAMETER = CalmVariable.Simple('DEFAULT_POSTGRES_PARAMS', is_hidden=True, runtime=False)
    NETWORK_PROFILE = CalmVariable.Simple('DEFAULT_OOB_POSTGRESQL_NETWORK', is_hidden=True, runtime=False)
    SOFTWARE_PROFILE = CalmVariable.Simple('POSTGRES_10.4_OOB', is_hidden=True, runtime=False)
    SLA_NAME = CalmVariable.Simple('NONE', is_hidden=True, runtime=False)

    DB_ID = CalmVariable.Simple('', is_hidden=True, runtime=False)
    DBSERVER_ID = CalmVariable.Simple('', is_hidden=True, runtime=False)
    DBSERVER_IP = CalmVariable.Simple('', is_hidden=True, runtime=False)


