from calm.dsl.builtins import Profile, CalmVariable

from deployments import AristaDeployment


class Default(Profile):

    deployments = [AristaDeployment]

    ARISTA_IP = CalmVariable.Simple('10.0.0.1', label='Arista IP Address', is_hidden=True, runtime=False)

    DOMAIN_NAME = CalmVariable.Simple('demo.lab', label='Domain Name', is_mandatory=True, runtime=True)
    DNS_SERVERS = CalmVariable.Simple('8.8.8.8', label='DNS Servers', is_mandatory=True, runtime=True, validate_regex=True,
                                      description='Comma separated ip address e.g. "8.8.8.8, 1.1.1.1"',
                                      regex='^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)|\*)(?:,\s*(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.(?:25[0-5]|2[0-4]\d|[01]?\d\d?)|\*))*$')
    ENABLE_DHCP = CalmVariable.WithOptions.Predefined(['Yes', 'No'], default='Yes', label='Enable DHCP',
                                                      is_mandatory=True, runtime=True)
    NETWORK_PREFIX = CalmVariable.WithOptions.Predefined(['24'], default='24', label='Network Prefix',
                                                  is_mandatory=True, runtime=True)
    IP_SUBNET = CalmVariable.Simple('', label='IP Subnet', is_mandatory=True, runtime=True, validate_regex=True,
                                    regex='^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:[0])$')
    CLUSTER_NAME = CalmVariable.WithOptions.Predefined(['Middle-East-Lab-cluster2'], default='Middle-East-Lab-cluster2',
                                                       label='Cluster', is_hidden=True, runtime=True)







