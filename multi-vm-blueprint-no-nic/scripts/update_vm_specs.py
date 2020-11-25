import requests

# -------------- Test Environment ------------------
# import urllib3
# urllib3.disable_warnings()
# vm_uuid = 'cc5c5a73-e7e2-410d-96ee-e0bd5b12d1a5'
# authorization = 'Basic YWRtaW46bngyVGVjaDkxMSE='
# url = 'https://10.38.2.9:9440/api/nutanix/v3/{}'
# vcpu = 2
# memory = 8*1024
# disk_size = 200*1024
# vm_network = {'kind': 'subnet', 'uuid': '5db23efe-f18f-4719-a525-39c1e823409e'}
# user_network_answer = 'yes'

# -------------- Calm Environment ------------------
vm_uuid = "@@{id}@@"
authorization = 'Bearer @@{calm_jwt}@@'
url = 'https://127.0.0.1:9440/api/nutanix/v3/{}'
vcpu = int("@@{cpunum}@@")
memory = int("@@{memorynum}@@")*1024
disk_size = int("@@{storage}@@")*1024
vm_network = json.loads('@@{VM_NETWORK}@@' if '@@{VM_NETWORK}@@' else '{}')
user_network_answer = '@@{INTERNET_ACCESS}@@'.lower()


kwargs = {
    'verify': False,
    'headers': {'Authorization': authorization}
}


# How do we handle cost showbacks on the instances?
###################### DO NOT MODIFY BELOW HERE ######################
#
######################     DEFINE FUNCTIONS     ######################
# define the function 'rest_call’
# this encapsulates the api call.

######################## GET VM SPEC ########################

resp = requests.get(url.format('vms/'+vm_uuid), **kwargs)
if resp.status_code == 200:
    print('INFO - get VM API was successful')
    response = resp.json()
else:
    print('ERROR - get vm api call failed, vm uuid: {}, status code: {}'.format(vm_uuid, resp.status_code))
    print('ERROR - Msg: {}'.format(resp.content))
    exit(1)


del response['status']
# update 'spec’ element in the 'response’ object with new vpcu and mem
response['spec']['resources']['num_sockets'] = vcpu
response['spec']['resources']['memory_size_mib'] = memory

# if user want network access add a nic from the VM_NETWORK
if user_network_answer.lower() == 'yes':
    nic_card = {'nic_type': 'NORMAL_NIC', 'vlan_mode': 'ACCESS',
                'subnet_reference': vm_network, 'is_connected': True}
    response['spec']['resources']['nic_list'] = [nic_card]
else:
    response['spec']['resources']['nic_list'] = []

# let’s address the space allocation on disk 0
del response['spec']['resources']['disk_list'][0]['disk_size_bytes']
response['spec']['resources']['disk_list'][0]['disk_size_mib'] = disk_size

resp = requests.put(url.format('vms/'+vm_uuid), json=response, **kwargs)
if resp.status_code == 202:
    print('INFO - VM updated was successful')
else:
    print('ERROR - VM uuid: {} update operation failed, status code: {}'.format(vm_uuid, resp.status_code))
    print('ERROR - Msg: {}'.format(resp.content))
    exit(1)
