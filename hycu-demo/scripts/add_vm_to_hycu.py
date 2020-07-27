#script

# Task name: Add a VM to HYCU backup group
# Description:  The propose of this script is to add the current VM to HYCU backup group for
#               for self-service setup. We assume the name of the group name in HYCU is the same
#               as the Calm project name.
#
# Required Calm variables: 
#   HYCU_IP: IP address of HYCU VM
#   HYCU: credentials object with premission to change VM ownership
# Version: v1.0
# Author: Husain Ebrahim <husain.ebrahim@nutanix.com>


# HYCU API call function
# ================================================================
def http_request(api_endpoint, payload='', method='POST'):
  username = '@@{HYCU.username}@@'
  password = '@@{HYCU.secret}@@'
  hycu_ip = '@@{HYCU_IP}@@'
  hycu_port = '8443'

  url = "https://{}:{}/rest/v1.0/{}".format(
      hycu_ip,
      hycu_port,
      api_endpoint
  )

  headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
  }

  if len(payload) > 0:
      payload = json.dumps(payload)


  resp = urlreq(
      url,
      verb=method,
      params=payload,
      headers=headers,
      auth='BASIC',
      user=username,
      passwd=password,
      verify=False
  )

  if resp.ok:
      return json.loads(resp.content), resp.ok
  else:
      print('Error in API call')
      print(resp)
      print(resp.content)
      return None, None

def find_vm_hycu_uuid(uuid):
    '''
        Find the HYCU UUID of the target VM by searching for AHV UUID
    '''
    vm_list, status = http_request('vms', method='GET')

    if not status:
        print('Error in UUID search API call')
        exit(1)

    for vm in vm_list['entities']:
        if vm['externalId'] == uuid:
            return vm['uuid']
    

def find_group_uuid(name):
    '''
        Find the uuid of the tenant group in HYCU, assuming same name as Calm project
    '''
    group_list, status = http_request('usergroups', method='GET')

    if not status:
        print('Error in find group uuid API call')
        exit(1)

    for group in group_list['entities']:
        if group['name'] == name:
            return group['uuid']
    

def update_hycu_vm_owner(group_uuid, vm_uuid):
    '''
        API call to update the VM ownership in HYCU
    '''
    endpoint = 'usergroups/{}'.format(group_uuid)
    payload = {
        'assignVirtualMachineIdsList': [vm_uuid]
    }
    result, status = http_request(endpoint, payload=payload)
    if not status:
        print('Error in VM onwership update API call')
        exit(1)
    return result['message']

ahv_uuid = '@@{id}@@'
project_name = '@@{calm_project_name}@@'

# delay 30sec
print('sleep for 30sec to sync VM uuid with HYCU')
sleep(30)
print('woke up')
# HYCU VM UUID
hycu_uuid = find_vm_hycu_uuid(ahv_uuid)
if not hycu_uuid:
    print('Error: AHV UUID not found in HYCU, make sure PE is added as source in HYCU')
    exit(1)
print('VM UUID in HYCU: {}'.format(hycu_uuid))

# HYCU Group UUID
group_uuid = find_group_uuid(project_name)
if not group_uuid:
    print('Error: Group UUID not found in HYCU for same Calm project name')
    exit(1)
print('Groupd UUID for {}: {}'.format(project_name, group_uuid))

# update HYCU ownership
result = update_hycu_vm_owner(group_uuid, hycu_uuid)
print(result['titleDescription'])