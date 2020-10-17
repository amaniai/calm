from calm.dsl.builtins import Service, CalmVariable, CalmTask, action


class DemoApp(Service):
    """CentOS based image"""
    OWNER = CalmVariable.Simple('', runtime=False)


class Haproxy(Service):
    """HAProxy service"""
    pass


class Postgres(Service):
    # Varaibles for DB provisioning
    SOFTWARE_ID = CalmVariable.Simple('', runtime=False)
    SOFTWARE_VERSION = CalmVariable.Simple('', runtime=False)
    COMPUTE_ID = CalmVariable.Simple('', runtime=False)
    NETWORK_ID = CalmVariable.Simple('', runtime=False)
    DB_PARAMETER = CalmVariable.Simple('', runtime=False)

    # Variables after initiating the DB
    OPERATION_ID = CalmVariable.Simple('', runtime=False)
