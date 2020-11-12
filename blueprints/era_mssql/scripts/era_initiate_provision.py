# Task name: Provision PostgreSQL on Era (single instance)
# Description:  The propose of this script is to provision Postgres DB on ERA
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
vm_name = 'era-mssql-{}'.format(dbserver_name)
db_password = '@@{DB_PASSWORD}@@'
vm_password = '@@{WINDOWS_CRED.secret}@@'
# vm_public_key = '@@{CENTOS_CRED.public_key}@@'

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
    'databaseType': 'sqlserver_database',
    'name': dbserver_name,
    'databaseDescription': 'Calm provisioned mssql DB',
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
        {'name': 'working_dir', 'value': 'C:\\temp'},
        {'name': 'database_size', 'value': '200'},
        {'name': 'sql_user_name', 'value': 'sa'},
        {'name': 'authentication_mode', 'value': 'windows'},
        {'name': 'delete_vm_on_failure', 'value': False},
        {'name': 'auto_tune_staging_drive', 'value': True},
        {'name': 'dbserver_description', 'value': 'Calm provisioned mssql DB'},
        {'name': 'dbserver_name', 'value': dbserver_name},
        {'name': 'server_collation', 'value': 'SQL_Latin1_General_CP1_CI_AS'},
        {'name': 'database_collation', 'value': 'SQL_Latin1_General_CP1_CI_AS'},
        {'name': 'dbParameterProfileIdInstance', 'value': 'e0529f3f-b9da-4738-b616-5372967d38c1'},
        {'name': 'vm_dbserver_admin_password', 'value': vm_password}
    ],
    'createDbserver': True,
    'nodeCount': 1,
    'nxClusterId': cluster_id,
    'clustered': False,
    'nodes': [{'properties': [], 'vmName': vm_name, 'networkProfileId': profiles['network']}],
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


