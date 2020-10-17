#script

# Task name: Delete a database using uuid
#
# Required Calm variables:
#   ERA_IP: IP address of ERA VM
#   ERA_CRED: credentials object with permission to access ERA
#   DB_ID: 
#
# Output variables:
#   OPERATION_UUID
#
# Version: v1.0
# Author: Husain Ebrahim <husain.ebrahim@nutanix.com>

import requests


def delete_database(db_uuid):
    payload = {
        'delete': True,
        'remove': False,
        'softRemove': False,
        'forced': False,
        'deleteTimeMachine': True,
        'deleteLogicalCluster': True
    }
    url = '{}/databases/{}'.format(base_url, db_uuid)
    resp = requests.delete(url, json=payload, **kwargs)
    if resp.status_code == 200:
        operation_id = resp.json()['operationId']
        print('Delete job started on Era')
        return operation_id
    else:
        print('Error - something is wrong with delete operation')
        print(resp.status_code, resp.content)
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
        print('DB_ENTITY_NAME={}'.format(entity_name))
        return entity_name


def delete_vm(dbserver_id):
    url = '{}/dbservers/{}'.format(base_url, dbserver_id)
    payload = {
        'softRemove': False,
        'remove': False,
        'delete': True,
        'deleteVgs': True,
        'deleteVmSnapshots': True
    }
    resp = requests.delete(url, json=payload, **kwargs)
    if resp.status_code == 200:
        operation_id = resp.json()['operationId']
        print('VM server delete job started')
        print('OPERATION_DI={}'.format(operation_id))
        return operation_id
    else:
        print('Error - somehting went wrong in VM delete on Era')
        print(resp.status_code, resp.content)
        exit(1)

# ##########################################################################################
# Main task function
# ##########################################################################################


base_url = 'https://@@{ERA_IP}@@/era/v0.9'
kwargs = {
    'verify': False,
    'auth': ('@@{ERA_CRED.username}@@', '@@{ERA_CRED.secret}@@')
}
DB_ID = '@@{DB_ID}@@'
DBSERVER_ID = '@@{DBSERVER_ID}@@'

operation_id = delete_database(DB_ID)
wait_for_operation(operation_id)
operation_id = delete_vm(DBSERVER_ID)
wait_for_operation(operation_id)


