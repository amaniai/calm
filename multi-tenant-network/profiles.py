from calm.dsl.builtins import Profile, CalmVariable

from deployments import AristaDeployment


class Default(Profile):

    deployments = [AristaDeployment]

    ARISTA_IP = CalmVariable.Simple('10.0.0.1', label='Arista IP Address', is_mandatory=True, runtime=True)


