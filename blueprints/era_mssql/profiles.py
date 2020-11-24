from calm.dsl.builtins import Profile, CalmVariable

from deployments import PostgresHAonEraDeployment
from vars import DB_PASSWORD_VALUE, ERA_PASSWORD_VALUE


class Production(Profile):

    deployments = [PostgresHAonEraDeployment]

    SLA_NAME = CalmVariable.WithOptions.Predefined(['NONE', 'DEFAULT_OOB_GOLD_SLA', 'DEFAULT_OOB_SILVER_SLA',
                                                    'DEFAULT_OOB_BRONZE_SLA', 'DEFAULT_OOB_BRASS_SLA'],
                                                   default='NONE', runtime=True)
    NETWORK_PROFILE = CalmVariable.WithOptions.Predefined(['PostGresNW'], default='PostGresNW', runtime=True)
    COMPUTE_PROFILE = CalmVariable.WithOptions.Predefined(['DEFAULT_OOB_COMPUTE', 'LOW_OOB_COMPUTE'],
                                                          default='LOW_OOB_COMPUTE', runtime=True)
    DB_NAME = CalmVariable.Simple('app', label='DB Name', is_mandatory=True, runtime=True)
    DBSERVER_NAME = CalmVariable.Simple('DB1', label='DB Server Name', is_mandatory=True, runtime=True)
    DB_PASSWORD = CalmVariable.Simple.Secret(DB_PASSWORD_VALUE, label='DB Password', is_mandatory=True, runtime=True)

    # hidden parameters
    DATABASE_PARAMETER = CalmVariable.Simple('DEFAULT_POSTGRES_PARAMS', is_hidden=True, runtime=False)
    SOFTWARE_PROFILE = CalmVariable.Simple('POSTGRES_10.4_OOB', is_hidden=True, runtime=False)
    ERA_IP = CalmVariable.Simple('10.42.32.40', label='ERA IP', is_mandatory=True, runtime=True, is_hidden=True)

    DB_ID = CalmVariable.Simple('', is_hidden=True, runtime=False)
    DBSERVER_ID = CalmVariable.Simple('', label='DB Server UUID', runtime=False, is_hidden=True)
    DBSERVER_IP = CalmVariable.Simple('', label='DB Server IP Address', runtime=False, is_hidden=True)


