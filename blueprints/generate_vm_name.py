# Name: Generate VM name based on xxx naming
# Task Type: set variable
# Script Type: EScript
# Author: Husain Ebrahim <husain.ebrahim@nutanix.com>
# Date: 01-08-2021
# Description:

import requests

# General script settings
# --------------------------------------------------
dc_name_category = 'DC_NAMES'
dc_name_undefined = 'XX'
counter_start = '01'
os_type = 'W'
server_type = 'V'

# -------------- Test Environment ------------------
import urllib3
urllib3.disable_warnings()
authorization = 'Basic xxx'
url = 'https://10.38.11.9:9440/api/nutanix/v3/{}'
project_name = 'default'
environment_name = 'Production'
application_type = 'SP'

# -------------- Calm Environment ------------------
# authorization = 'Bearer @@{calm_jwt}@@'
# url = 'https://127.0.0.1:9440/api/nutanix/v3/{}'
# project_name = '@@{calm_project_name}@@'
# environment_name = '@@{calm_environment_name}@@'
# application_type = '@@{APPLICATION_TYPE}@@'

kwargs = {
    'verify': False,
    'headers': {'Authorization': authorization}
}

# get default subnet from environment + project name
payload = {'kind': 'environment'}
r = requests.post(url.format('environments/list'), json=payload, **kwargs)
if r.status_code == 200:
    subnet_uuid = None
    for env in r.json()['entities']:
        if env['metadata']['project_reference']['name'] == project_name and env['metadata']['name'] == environment_name:
            # TODO: assuming only one infra_inclusion_list item
            subnet_uuid = env['status']['resources']['infra_inclusion_list'][0]['default_subnet_reference']['uuid']
            break
else:
    print('ERROR - enviornment API call failed, status code: {}, message: {}'.format(r.status_code, r.content))

# get DC from subnet category
if subnet_uuid:
    payload = {'kind': 'subnet'}
    r = requests.post(url.format('subnets/list'), json=payload, **kwargs)
    if r.status_code == 200:
        dc_name = None
        for subnet in r.json()['entities']:
            if subnet['metadata']['uuid'] == subnet_uuid:
                dc_name = subnet['metadata']['categories'].get(dc_name_category, dc_name_undefined)
                break
    else:
        print('ERROR - subnet API call failed, status code: {}, message: {}'.format(r.status_code, r.content))
        dc_name = dc_name_undefined
else:
    print('No default subnet found')
    dc_name = dc_name_undefined

vm_name_prefix = environment_name[:1].upper() + dc_name[:2].upper() + '-' + project_name[:3].upper() + '-' + os_type[:1].upper() + server_type[:1].upper() + '-' + application_type[:2].upper()

# get next available index for VM name
payload = {
    'kind': 'vm',
    'filter': 'vm_name=={}.*'.format(vm_name_prefix),
    'sort_order': 'DESCENDING',
    'sort_attribute': 'vm_name'
}
resp = requests.post(url.format('vms/list'), json=payload, **kwargs)
if resp.status_code == 200:
    vm_list = resp.json()['entities']
    print('INFO - Prism has: {} vms starting with {}'.format(len(vm_list), vm_name_prefix))
    if len(vm_list):
        try:
            # vm_name = vm_list[0]['spec']['name']
            current_count = int(vm_list[0]['spec']['name'][-2:])
            print('INFO - last vm unique count: {}'.format(current_count))
            next_count = '{0:0=2d}'.format(current_count+1)
            print('VM_NAME={}{}'.format(vm_name_prefix, next_count))
            exit(0)
        except Exception as error:
            print('ERROR - Last VM name does not match the expected pattern, vm name: {}'.format(vm_name_prefix))
            print('ERROR - msg:{}'.format(error))
else:
    print('ERROR - API call failed, status code: {}, message: {}'.format(resp.status_code, resp.content))

print('INFO - not able to get latest vm count, falling back to default')
print('VM_NAME={}'.format(vm_name_prefix+counter_start))