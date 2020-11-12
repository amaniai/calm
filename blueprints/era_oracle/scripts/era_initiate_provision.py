# Task name: Provision Oracle on Era (single instance)
# Description:  The propose of this script is to provision Oracle DB on ERA
#
# Version: v1.0
# Author: Husain Ebrahim <husain.ebrahim@nutanix.com>

# ERA API call function
# ================================================================
import requests
# from pprint import pprint
# from time import sleep


base_url = 'https://@@{ERA_IP}@@/era/v0.9'
kwargs = {
    'verify': False,
    'auth': ('@@{ERA_USERNAME}@@', '@@{ERA_PASSWORD}@@')
}

db_name = '@@{DB_NAME}@@'
dbserver_name = '@@{DBSERVER_NAME}@@'
vm_name = 'era-oracle-{}'.format(dbserver_name)
db_password = '@@{DB_PASSWORD}@@'
vm_public_key = '@@{CENTOS_CRED.public_key}@@'
sid_name = '@@{SID_NAME}@@'

cluster_id = '@@{CLUSTER_ID}@@'
profiles = {
    'software': '@@{SOFTWARE_ID}@@',
    'software_version': '@@{SOFTWARE_VERSION}@@',
    'compute': '@@{COMPUTE_ID}@@',
    'network': '@@{NETWORK_ID}@@',
    'db_parameter': '@@{DB_PARAMETER}@@',
    'sla_id': '@@{SLA_ID}@@'
}

payload = {
    'databaseType': 'oracle_database',
    'name': dbserver_name,
    'databaseDescription': 'Calm provisioned Oracle DB',
    'softwareProfileId': profiles['software'],
    'softwareProfileVersionId': profiles['software_version'],
    'computeProfileId': profiles['compute'],
    'networkProfileId': profiles['network'],
    'dbParameterProfileId': profiles['db_parameter'],
    'newDbServerTimeZone': 'UTC',
    'timeMachineInfo': {
        'name': '{}_TM'.format(dbserver_name),
        'description': '',
        'slaId': profiles['sla_id'],
        'tags': [],
        'autoTuneLogDrive': True,
        'schedule': {
            'snapshotTimeOfDay': {'hours': 1, 'minutes': 0, 'seconds': 0},
            'continuousSchedule': {'enabled': True, 'logBackupInterval': 30, 'snapshotsPerDay': 1},
            'weeklySchedule': {'enabled': True, 'dayOfWeek': 'TUESDAY'},
            'monthlySchedule': {'enabled': True, 'dayOfMonth': '13'},
            'quartelySchedule': {'enabled': True, 'startMonth': 'JANUARY', 'dayOfMonth': '13'},
            'yearlySchedule': {'enabled': False, 'dayOfMonth': 31, 'month': 'DECEMBER'}
        }
    },
    'actionArguments': [
        {'name': 'listener_port', 'value': '1521'},
        {'name': 'database_size', 'value': '200'},
        {'name': 'enable_tde', 'value': False},
        {'name': 'db_character_set', 'value': 'AL32UTF8'},
        {'name': 'national_character_set', 'value': 'AL16UTF16'},
        {'name': 'working_dir', 'value': '/tmp'},
        {'name': 'enable_ha', 'value': False},
        {'name': 'auto_tune_staging_drive', 'value': True},
        {'name': 'enable_cdb', 'value': False},
        {'name': 'database_fra_size', 'value': '200'},
        {'name': 'dbserver_name', 'value': dbserver_name},
        {'name': 'global_database_name', 'value': sid_name},
        {'name': 'oracle_sid', 'value': sid_name},
        {'name': 'dbserver_description', 'value': 'Calm provisioned Oracle DB'},
        {'name': 'sys_password', 'value': db_password},
        {'name': 'system_password', 'value': db_password},
    ],
    'createDbserver': True,
    'nodeCount': 1,
    'nxClusterId': cluster_id,
    'sshPublicKey': vm_public_key,
    'clustered': False,
    'autoTuneStagingDrive': True
}
print(payload)
url = '{}/databases/provision'.format(base_url)
resp = requests.post(url, json=payload, **kwargs)
if resp.status_code == 200:
    operation_id = resp.json()['operationId']
    entity_id = resp.json()['entityId']
    entity_name = resp.json()['entityName']
    print('OPERATION_ID={}'.format(operation_id))
else:
    print('error while provision DB ...')
    print(resp.content)
    exit(1)


