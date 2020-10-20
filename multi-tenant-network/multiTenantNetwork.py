import json
import sys

from calm.dsl.builtins import Blueprint
from calm.dsl.cli.bps import compile_blueprint, create_blueprint
from calm.dsl.api.handle import get_api_client

from vars import ARISTA_CRED, PC_CRED
from services import Arista
from packages import AristaPackage
from substrates import AristaSubstrate
from profiles import Default


class MultiTenantNetwork(Blueprint):
    """Demo app blueprint"""
    profiles = [Default]
    services = [Arista]
    substrates = [AristaSubstrate]
    packages = [AristaPackage]
    credentials = [ARISTA_CRED, PC_CRED]


def main():
    blueprin_obj = compile_blueprint(__file__)
    print('blueprint compiled successfully... ')
    
    client = get_api_client()
    res, _ = create_blueprint(client, blueprin_obj, force_create=True)
    
    bp = res.json()
    bp_uuid = bp['metadata']['uuid']
    bp_name = bp['metadata']['name']
    bp_status = bp.get('status', {})
    bp_state = bp_status.get('state', 'DRAFT')
    print('Blueprint {} has state: {}'.format(bp_name, bp_state))

    if bp_state != 'ACTIVE':
        msg_list = bp_status.get('message_list', [])
        if not msg_list:
            print(f'Blueprint {bp_name} created with errors.')
            print(json.dumps(bp_status))
            sys.exit(-1)

        msgs = []
        for msg_dict in msg_list:
            msgs.append(msg_dict.get('message', ''))

        print(f'Blueprint {bp_name} created with {len(msg_list)} error(s): {msgs}')
        sys.exit(-1)

    print(f'Blueprint {bp_name}, uuid: {bp_uuid} created successfully.')


if __name__ == '__main__':
    main()
