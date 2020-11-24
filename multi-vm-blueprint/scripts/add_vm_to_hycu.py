#script

# Task name: Add a VM to HYCU backup group
# Description:  The propose of this script is to add the current VM to HYCU backup group for
#               for self-service setup. We assume the name of the group name in HYCU is the same
#               as the Calm project name.
#
# Required Calm variables: 
#   HYCU_IP: IP address of HYCU VM
#   HYCU_PORT: Port of HYCU web service
#   HYCU_CRED: credentials object with premission to change VM ownership
# Version: v1.1
# Author: Husain Ebrahim <husain.ebrahim@nutanix.com>

import requests

# variables from the environment
prism_vm_uuid = '@@{id}@@'
prism_project_name = '@@{calm_project_name}@@'
exit_code_if_not_found = 0
hycu_ip = '@@{HYCU_IP}@@'
hycu_port = '@@{HYCU_PORT}@@'
verify_ssl = False
hycu_user = '@@{HYCU_CRED.username}@@'
hycu_pass = '@@{HYCU_CRED.secret}@@'

# calculated values
hycu_baseurl = 'https://{}:{}/rest/v1.0'.format(hycu_ip, hycu_port)
hycu_vm_uuid = None
hycu_group_uuid = None

# wait for hycu to sync VM uuids
sleep(240)

# get VM HYCU uuid from Prism uuid
url = '{}/vms'.format(hycu_baseurl)
resp = requests.get(url, auth=(hycu_user, hycu_pass), verify=verify_ssl)
if resp.status_code == 200:
    print('INFO - VM list from hycu successful.')
    vms = resp.json()['entities']
    print('INFO - Found: {} VMs'.format(len(vms)))
    for vm in vms:
        if vm['externalId'] == prism_vm_uuid:
            print('INFO - VM: {} has uuid: {} in Hycu'.format(prism_vm_uuid, vm['uuid']))
            hycu_vm_uuid = vm['uuid']
            break
    
    # check if the VM is not found
    if not hycu_vm_uuid:
        print('Error - VM: {} not found in hycu'.format(prism_vm_uuid))
        exit(exit_code_if_not_found)
else:
    print('Error in listing VMs from HYCU, status code: {}'.format(resp.status_code))
    print(resp.content)
    exit(1)

# find the group uuid in hycu
url = '{}/usergroups'.format(hycu_baseurl)
resp = requests.get(url, auth=(hycu_user, hycu_pass), verify=verify_ssl)
if resp.status_code == 200:
    print('INFO - user groups list successful')
    groups = resp.json()['entities']
    print('INFO - Found: {} groups'.format(len(groups)))
    for group in groups:
        if group['name'] == prism_project_name:
            print('INFO - Prism project {}, has a group uuid: {} in hycu'.format(prism_project_name, group['uuid']))
            hycu_group_uuid = group['uuid']
            break

    # no group found for this project
    if not hycu_group_uuid:
        print('Error - no group for Prism project: {}'.format(prism_project_name))
        exit(exit_code_if_not_found)
else:
    print('Error in group listing from HYCU, status code: {}'.format(resp.status_code))
    print(resp.content)
    exit(1)

# assign VM to the user group
url = '{}/usergroups/{}'.format(hycu_baseurl, hycu_group_uuid)
payload = {'assignVirtualMachineIdsList': [hycu_vm_uuid]}
resp = requests.post(url, json=payload, auth=(hycu_user, hycu_pass), verify=verify_ssl)

if resp.status_code == 200:
    print('INFO - VM owner updated')
    print('INFO - result message: {}'.format(resp.json().get('message').get('titleDescription')))
else:
    print('Error - in hycu onwer update, status code: {}'.format(resp.status_code))
    print(resp.content)
    exit(1)

