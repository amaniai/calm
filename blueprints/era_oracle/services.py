from calm.dsl.builtins import Service, CalmVariable


class Oracle(Service):
    # Variables for DB provisioning
    ERA_USERNAME = CalmVariable.Simple('', runtime=False)
    ERA_PASSWORD = CalmVariable.Simple.Secret('', runtime=False)
    SOFTWARE_ID = CalmVariable.Simple('', runtime=False)
    SOFTWARE_VERSION = CalmVariable.Simple('', runtime=False)
    COMPUTE_ID = CalmVariable.Simple('', runtime=False)
    NETWORK_ID = CalmVariable.Simple('', runtime=False)
    DB_PARAMETER = CalmVariable.Simple('', runtime=False)

    # Variables after initiating the DB
    OPERATION_ID = CalmVariable.Simple('', runtime=False)
