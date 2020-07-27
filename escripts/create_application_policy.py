#script

# Task name: Create a secuirty policy based on project and application name
# Description: 
#
# Required Calm variables: 
#   None
# Version: v1.0
# Author: Husain Ebrahim <husain.ebrahim@nutanix.com>


# Prism API call function
# ================================================================
def http_request(api_endpoint, payload='', method='POST'):
  jwt = '@@{calm_jwt}@@'
  pc_address = '127.0.0.1'
  pc_port = '9440'

  url = "https://{}:{}/api/nutanix/v3/{}".format(
    pc_address,
    pc_port,
    api_endpoint
  )

  headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer {}'.format(jwt)
  }

  if len(payload) > 0:
    payload = json.dumps(payload)


  resp = urlreq(
    url,
    verb=method,
    params=payload,
    headers=headers,
    verify=False
  )

  if resp.ok:
    return json.loads(resp.content), resp.ok
  else:
    print('Error in API call')
    print(resp)
    print(resp.content)


def add_category_key(category_name, category_key):
  payload = {'value': category_key}
  _, status = http_request('categories/{}/{}'.format(category_name, category_key), payload=payload, method='PUT')
  if status:
    return True
  else:
    return False


def update_vm_category(vm_uuid, category_name, cateogry_key):
  resp, status = http_request('vms/{}'.format(vm_uuid), method='GET')
  if status:
    payload = {
      'spec': resp['spec'],
      'api_version': resp['api_version'],
      'metadata': resp['metadata']
    }
  else:
    print('Error getting VM details from Prism')
    exit(1)

  payload['metadata']['categories'][category_name] = category_key

  result, status = http_request('vms/{}'.format(vm_uuid), payload=payload, method='PUT')

  return result, status


def generate_ace(ace):
  ip = ace.get('ip')
  prefix = int(ace.get('prefix', 0))
  proto = ace.get('protocol')
  port = int(ace.get('port', 0))
  entry = {
    'peer_specification_type': 'IP_SUBNET',
    'ip_subnet': {
      'ip': ip,
      'prefix_length': prefix
    },
    'protocol': proto,
  }
  
  if proto == 'TCP':
    entry['tcp_port_range_list'] = [{'start_port': port, 'end_port': port}]
  elif proto == 'UDP':
    entry['udp_port_range_list'] = [{'start_port': port, 'end_port': port}]

  return entry

def create_security_policy(category_name, category_key, description='', base_acl=[]):
  name = 'calm-{}'.format(category_key)
  if len(description) == 0:
      description = name

  target_group = {
    'peer_specification_type': 'FILTER',
    'filter': {
      'type': 'CATEGORIES_MATCH_ALL',
      'kind_list': ['vm'],
      'params': {category_name: [category_key]}
    }
  }

  resources = {
    'allow_ipv6_traffic': False,
    'is_policy_hitlog_enabled': False,
    'app_rule': {
      'target_group': target_group,
      'inbound_allow_list': [],
      'outbound_allow_list': [{'peer_specification_type': 'ALL'}],
      'action': 'APPLY'
    }
  }

  acl = []
  for ace in base_acl:
    acl.append(generate_ace(ace))

  resources['app_rule']['inbound_allow_list'] = acl

  payload = {
    'api_version': '3.1.0',
    'metadata': {'kind': 'network_security_rule'},
    'spec': {
      'name': name,
      'description': description,
      'resources': resources
    }
  }

  resp, status =  http_request('network_security_rules', payload=payload)
  return resp, status

# ##########################################################################################
# Main task function
# ##########################################################################################

project_name = re.sub('[\W_]+', '', '@@{calm_project_name}@@')
app_name = re.sub('[\W_]+', '', '@@{calm_application_name}@@')
description = 'Project name: {}, Application name: {}'.format('@@{calm_project_name}@@'
                                                      ,'@@{calm_application_name}@@')
random_num = '@@{calm_random}@@'
vm_uuid = '@@{id}@@'

category_name = 'AppType'
category_key = '{}-{}-{}'.format(project_name, app_name, random_num)
result = add_category_key(category_name, category_key)
if result:
  print('New key created in category: {}, value: {}'.format(category_name, category_key))
else:
  print('Error while creating a new key')
  exit(1)

resp, status = update_vm_category(vm_uuid, category_name, category_key)
if status:
  print('VM updated with category')
else:
  print('Error in updating the VM category')
  exit(1)

# Base ACL here to allow Calm to manage VMs over ssh and powershell
base_acl = [
  {'ip': '0.0.0.0', 'prefix': 0, 'protocol': 'TCP', 'port': 22},
  {'ip': '0.0.0.0', 'prefix': 0, 'protocol': 'TCP', 'port': 5985},
]

resp, status = create_security_policy(category_name, category_key, description, base_acl)
if status:
  print('Security policy created ...')
  print('POLICY_UUID={}'.format(resp['metadata']['uuid']))
  print('INBOUND_ACL={}'.format(json.dumps(base_acl)))
else:
  print('Error in creating the policy')
  exit(1)
