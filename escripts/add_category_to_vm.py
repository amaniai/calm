#script

# Task name: Update Calm service category with project name
# Description: The propose of this task is to update the current service executing the 
# task with the project name as a category key in a specified category name. The objective 
# is to allow security policies to be applied based on Calm projects. 
# Note: assuming Project Name complies with category values naming convention
#
# Required Calm variables: 
#   CATEGORY_NAME: (str)
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



def check_category(category_name):
  '''
  This function checks if the category name exists in Prism.
    Parameters:
      category_name (str): Name of the category to search for
    Returns:
      result (bool): True if name if found
  '''

  result, status = http_request('categories/{}'.format(category_name), method='GET')
  if status:
      if result.get('name') == category_name:
        return True
  else:
    return False


def list_category_keys(category_name):
    payload = {'kind': 'category'}
    result, status = http_request('categories/{}/list'.format(category_name), payload=payload)
    if status:
      keys_list = []
      for category in result.get('entities', []):
          keys_list.append(category['value'])
      return keys_list
    else:
      print('Error in getting the list of category keys')
      return False

def add_category_key(category_name, category_key):
    payload = {'value': category_key}
    result, status = http_request('categories/{}/{}'.format(category_name, category_key), payload=payload, method='PUT')
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


def generate_unique_name(project_name):
  unique_id = base64.b64encode(project_name).decode().replace('+', '').replace('/', '').replace('=', '')
  category_name = re.sub('[\W_]+', '', project_name)
  return '{}-{}'.format(category_name, unique_id)

# ##########################################################################################
# Main task function
# ##########################################################################################

category_name = '@@{CATEGORY_NAME}@@'
category_key = generate_unique_name('@@{calm_project_name}@@')
vm_uuid = '@@{id}@@'
# check if category name exists
if check_category(category_name):
  print('Category already exists in Prism ...')
else:
  print('Error: category does not existings in Prism')
  exit(1)

print("Listing keys ...")
current_keys = list_category_keys(category_name)
print(current_keys)

if category_key not in current_keys:
    print('Key not there, updating category')
    add_category_key(category_name, category_key)
    current_keys = list_category_keys(category_name)
    print(current_keys)

_, status = update_vm_category(vm_uuid, category_name, category_key)
if status:
  print('VM updated with category')
else:
  print('Error in updating the VM category')
  exit(1)
