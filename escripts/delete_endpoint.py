# Name: delete endpoint based on name
# Task Type: execute
# Script Type: EScript
# Author: Husain Ebrahim <husain.ebrahim@nutanix.com>
# Date: 22-08-2021
# Description:

import requests

# General script settings
# --------------------------------------------------

# -------------- Test Environment ------------------
# import urllib3
# urllib3.disable_warnings()
# authorization = 'Basic xxxxxxx'
# url = 'https://10.0.0.98:9440/api/nutanix/v3/{}'
# endpoint_name = 'VM-test-123'

# -------------- Calm Environment ------------------
authorization = 'Bearer @@{calm_jwt}@@'
url = 'https://127.0.0.1:9440/api/nutanix/v3/{}'
endpoint_name = '@@{name}@@'

kwargs = {
    'verify': False,
    'headers': {'Authorization': authorization}
}

# get endpoint uuid
payload = {
  'kind': 'endpoint',
  'filter': 'name=={}'.format(endpoint_name)
}

r = requests.post(url.format('endpoints/list'), json=payload, **kwargs)
if r.status_code == 200 and len(r.json()['entities']):
  endpoint_uuid = r.json()['entities'][0]['metadata']['uuid']
  print('INFO - endpoint uuid: {}'.format(endpoint_uuid))
else:
  print('ERROR endpoint uuid fetch failed, status code: {}, message: {}'.format(r.status_code, r.content))
  exit(0)

# deleting the endpoint
r = requests.delete(url.format('endpoints/'+endpoint_uuid), **kwargs)
if r.status_code == 200:
  print('INFO - endpoint {} deleted'.format(endpoint_name))
else:
  print('ERROR - endpoint delete failed, status code: {}, message: {}'.format(r.status_code, r.content))
