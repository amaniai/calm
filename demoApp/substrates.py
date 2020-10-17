from calm.dsl.builtins import Substrate, readiness_probe, read_provider_spec, ref, action, CalmTask

from base_vm import CentOSAhvVM
from vars import CENTOS_CRED


class DemoAppVMS(Substrate):
    """CentOS substrate"""

    provider_spec = CentOSAhvVM


class HaproxyVMS(Substrate):
    """HAProxy substrate"""
    provider_spec = CentOSAhvVM


class PostgresEraSubstrate(Substrate):

    os_type = 'Linux'
    provider_type = 'EXISTING_VM'
    provider_spec = read_provider_spec('specs/postgres_era.yaml')

    readiness_probe = readiness_probe(
        connection_type='SSH',
        disabled=True,
        retries='5',
        connection_port=22,
        address='@@{ip_address}@@',
        delay_secs='60',
        credential=ref(CENTOS_CRED)
    )

    @action
    def __pre_create__(self):
        CalmTask.SetVariable.escript(filename='scripts/era_get_profile_ids.py', name='get profile ids',
                                     variables=['CLUSTER_ID', 'SOFTWARE_ID', 'SOFTWARE_VERSION', 'COMPUTE_ID',
                                                'NETWORK_ID', 'DB_PARAMETER', 'SLA_ID'])
        CalmTask.SetVariable.escript(filename='scripts/era_initiate_provision.py', name='initiate db provision',
                                     variables=['OPERATION_ID'])

        CalmTask.Exec.escript(filename='scripts/era_wait_for_operation.py', name='wait for operation')
        CalmTask.SetVariable.escript(filename='scripts/era_get_db_details.py', name='get db details',
                                     variables=['DB_ID', 'DBSERVER_ID', 'DBSERVER_IP'])


    @action
    def __post_delete__(self):
        CalmTask.Exec.escript(filename='scripts/era_delete_database.py', name='delete_postgres')



