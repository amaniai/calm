#script

# Task name: List category keys
# Description: List all existing keys in a given cateogry name in Prism
# Required Calm variables: 
#   CATEGORY_NAME: (str)
#   PRISM_AUTH: credentials to login to Prism API
# Version: v1.0
# Author: Husain Ebrahim <husain.ebrahim@nutanix.com>


# Prism API call function
# ================================================================
def http_request(api_endpoint, payload='', method='POST'):
  username = '@@{PRISM_AUTH.username}@@'
  password = '@@{PRISM_AUTH.secret}@@'
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
  }

  if len(payload) > 0:
      payload = json.dumps(payload)


  resp = urlreq(
      url,
      verb=method,
      params=payload,
      headers=headers,
      verify=False,
      auth='BASIC',
      user=username,
      passwd=password
  )

  if resp.ok:
      return json.loads(resp.content), resp.ok
  else:
      print('Error in API call')




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


# ##########################################################################################
# Main task function
# ##########################################################################################

category_name = '@@{CATEGORY_NAME}@@'
keys_list = list_category_keys(category_name)
output = ', '
print(', '.join(keys_list))

