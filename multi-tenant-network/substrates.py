from calm.dsl.builtins import Substrate, readiness_probe, read_provider_spec, ref, action, CalmTask

from vars import ARISTA_CRED


class AristaSubstrate(Substrate):

    os_type = 'Linux'
    provider_type = 'EXISTING_VM'
    provider_spec = read_provider_spec('specs/arista_specs.yaml')

    readiness_probe = readiness_probe(
        connection_type='SSH',
        disabled=True,
        retries='5',
        connection_port=22,
        address='@@{ip_address}@@',
        delay_secs='60',
        credential=ref(ARISTA_CRED)
    )



