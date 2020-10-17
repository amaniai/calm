# Task name: Provision PostgreSQL on Era (single instance)
# Description:  The propose of this script is to provision Postgres DB on ERA
#
# Required Calm variables:
#   ERA_IP: IP address of ERA VM
#   ERA_CRED: credentials object with permission to access ERA
#   DB_NAME: name of the database
#   DB_PASSWORD
#   OS_CRED
#
#   Optional Calm variables:
#   SOFTWARE_PROFILE
#   COMPUTE_PROFILE
#   NETWORK_PROFILE
#   DATABASE_PARAMETER
#
# Output variables:
#   CLUSTER_UUID
#
# Version: v1.0
# Author: Husain Ebrahim <husain.ebrahim@nutanix.com>

# ERA API call function
# ================================================================
import requests
# from pprint import pprint
# from time import sleep


def get_cluster_id (name=''):
    url = '{}/clusters'.format(base_url)
    resp = requests.get(url, **kwargs)
    if resp.status_code == 200:
        return resp.json()[0]['id']


def get_all_parameters():
    url = '{}/profiles'.format(base_url)
    resp = requests.get(url, **kwargs)
    if resp.status_code == 200:
        for profile in resp.json():
            if profile['topology'] == 'ALL' or profile['topology'] == 'single':
                if profile['engineType'] == 'Generic' or profile['engineType'] == 'postgres_database':
                    profiles[profile['type'].lower()] = {'id': profile['id'],
                                                         'name': profile['name'],
                                                         'version': profile['versions'][0]['id']}

    return profiles


def get_sla_id(sla_name='NONE'):
    url = '{}/slas'.format(base_url)
    resp = requests.get(url, **kwargs)

    if resp.status_code:
        for sla in resp.json():
            if sla['name'] == sla_name:
                return sla['id']


def provision_db():
    payload = {
        'databaseType': 'postgres_database',
        'name': dbserver_name,
        'databaseDescription': 'Calm provisioned postgres DB',
        'softwareProfileId': profiles['software']['id'],
        'softwareProfileVersionId': profiles['software']['version'],
        'computeProfileId': profiles['compute']['id'],
        'networkProfileId': profiles['network']['id'],
        'dbParameterProfileId': profiles['database_parameter']['id'],
        'newDbServerTimeZone': 'UTC',
        'timeMachineInfo': {
            'name': '{}_TM'.format(dbserver_name),
            'description': '',
            'slaId': sla_id,
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
            {'name': 'listener_port', 'value': '5432'},
            {'name': 'database_size', 'value': '200'},
            {'name': 'auto_tune_staging_drive', 'value': True},
            {'name': 'cluster_database', 'value': False},
            {'name': 'dbserver_description', 'value': 'Calm provisioned postgres DB'},
            {'name': 'database_names', 'value': db_name},
            {'name': 'db_password', 'value': db_password},
        ],
        'createDbserver': True,
        'nodeCount': 1,
        'nxClusterId': cluster_id,
        'sshPublicKey': vm_public_key,
        'clustered': False,
        'nodes': [{'properties': [], 'vmName': vm_name, 'networkProfileId': profiles['network']['id']}],
        'autoTuneStagingDrive': True
    }
    pprint(payload)
    url = '{}/databases/provision'.format(base_url)
    resp = requests.post(url, json=payload, **kwargs)
    if resp.status_code == 200:
        operation_id = resp.json()['operationId']
        entity_id = resp.json()['entityId']
        entity_name = resp.json()['entityName']
        print('OPERATION_ID={}'.format(operation_id))
        return operation_id, entity_id, entity_name
    else:
        print('error while provision DB ...')
        print(resp.content)
        exit(1)


def wait_for_operation(provision_id):
    url = '{}/operations/{}'.format(base_url, provision_id)
    for x in range(20):
        sleep(60)
        resp = requests.get(url, **kwargs)
        if resp.status_code == 200:
            job_percent = resp.json()['percentageComplete']
            job_status = resp.json()['status']
            print('Percentage Complete: {}'.format(job_percent))
            if job_percent == '100':
                print('Operation:{} completed successfully ...'.format(operation_id))
                break
            elif job_status != '1':
                print('Error - something went wrong with operation: {}'.format(operation_id))
                exit(1)

    if job_percent != '100':
        print('Error - Operation:{} timed-out '.format(operation_id))
        exit(1)
    else:
        entity_name = resp.json()['entityName']
        return entity_name


def get_db_ip_address(db_id):
    url = '{}/databases/{}'.format(base_url, db_id)
    resp = requests.get(url, **kwargs)
    vm_ip = ''
    if resp.status_code == 200:
        for item in resp.json()['properties']:
            if item['name'] == 'vm_ip':
                vm_ip = item['value']
        dbserver_id = resp.json()['databaseNodes'][0]['dbserverId']
        return dbserver_id, vm_ip


# ##########################################################################################
# Main task function
# ##########################################################################################

base_url = 'https://@@{ERA_IP}@@/era/v0.9'
kwargs = {
    'verify': False,
    'auth': ('@@{ERA_CRED.username}@@', '@@{ERA_CRED.secret}@@')
}
profiles = {
    'software': {'name': '@@{SOFTWARE_PROFILE}@@', 'id': ''},
    'compute': {'name': '@@{COMPUTE_PROFILE}@@', 'id': ''},
    'network': {'name': '@@{NETWORK_PROFILE}@@', 'id': ''},
    'database_parameter': {'name': '@@{DATABASE_PARAMETER}@@', 'id': ''},
    'storage': {'name': '', 'id': ''}
}

db_name = '@@{DB_NAME}@@'
dbserver_name = '@@{DBSERVER_NAME}@@'
vm_name = 'era-pstgr-{}'.format(dbserver_name)
db_password = '@@{DB_PASSWORD}@@'
vm_public_key = '@@{CENTOS_CRED.public_key}@@'

cluster_id = get_cluster_id()
profiles = get_all_parameters()
print('obtained profiles from Era')
sla_id = get_sla_id()
print('obtained sla_id from Era')
print('--------------------------')
operation_id, db_id, db_name = provision_db()
print('Provision job submitted successfully {}'.format(operation_id))
wait_for_operation(operation_id)
dbserver_id, dbserver_ip = get_db_ip_address(db_id)
print('DB_ID={}'.format(db_id))
print('DBSERVER_ID={}'.format(dbserver_id))
print('DBSERVER_IP={}'.format(dbserver_ip))

