import json
import sys

from calm.dsl.builtins import Blueprint
from calm.dsl.cli.bps import compile_blueprint, create_blueprint
from calm.dsl.api.handle import get_api_client

from vars import CENTOS_CRED, ERA_CRED
from services import DemoApp, Haproxy, Postgres
from packages import DemoAppPackage, HaproxyPackage, PostgresPackage
from substrates import DemoAppVMS, HaproxyVMS, PostgresEraSubstrate
from profiles import Production


class DemoApp(Blueprint):
    """Demo app blueprint"""
    profiles = [Production]
    services = [DemoApp, Haproxy, Postgres]
    substrates = [DemoAppVMS, HaproxyVMS, PostgresEraSubstrate]
    packages = [DemoAppPackage, HaproxyPackage, PostgresPackage]
    credentials = [CENTOS_CRED, ERA_CRED]


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
