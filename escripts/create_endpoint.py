# Name: Create endpoint based on VM IP
# Task Type: set variable
# Script Type: EScript
# Author: Husain Ebrahim <husain.ebrahim@nutanix.com>
# Date: 22-08-2021
# Description:

import requests

# General script settings
# --------------------------------------------------
# linux OS
endpoint_type = 'Linux'
endpoint_port = '22'

# Windows OS
# endpoint_type = 'Windows'
# endpoint_port = '5985'

# -------------- Test Environment ------------------
# import urllib3
# urllib3.disable_warnings()
# authorization = 'Basic xxxx'
# url = 'https://10.0.0.98:9440/api/nutanix/v3/{}'
# project_name = 'TVTC'
# endpoint_name = 'VM-test-1234'
# endpoint_address = '10.21.21.181'
# endpoint_username = 'administrator'
# endpoint_password = 'xxxxxx'

# -------------- Calm Environment ------------------
authorization = 'Bearer @@{calm_jwt}@@'
url = 'https://127.0.0.1:9440/api/nutanix/v3/{}'
project_name = '@@{calm_project_name}@@'
endpoint_name = '@@{name}@@'
endpoint_address = '@@{address}@@'
endpoint_username = '@@{CRED.username}@@'
endpoint_password = '@@{CRED.secret}@@'

kwargs = {
    'verify': False,
    'headers': {'Authorization': authorization}
}

# get project uuid
payload = {
    'filter': 'name=={}'.format(project_name),
    'kind': 'project'
}

project_uuid = None
r = requests.post(url.format('projects/list'), json=payload, **kwargs)
if r.status_code == 200:
    print('INFO - got project UUID')
    project_uuid = r.json()['entities'][0]['metadata']['uuid']
    print('INFO - project uuid: {}'.format(project_uuid))
else:
    print('ERROR - API call failed, status code: {}, message: {}'.format(r.status_code, r.content))
    exit(0)


# create endpoint entry
payload = {
  'spec': {
    'name': endpoint_name,
    'description': 'Endpoint for vm {}, ip address: {}'.format(endpoint_name, endpoint_address),
    'resources': {
      'name': endpoint_name,
      'type': endpoint_type,
      'attrs': {
        'values': [ endpoint_address ],
        'value_type': 'IP',
        'port': endpoint_port,
        'credential_definition_list': [
          {
            'name': 'endpoint_cred',
            'description': endpoint_username,
            'type': 'KEY',
            'username': endpoint_username,
            'secret': {
              'attrs': {
                'is_secret_modified': False
              }
            }
          }
        ],
        'login_credential_reference': {
          'kind': 'app_credential',
          'name': 'endpoint_cred'
        }
      }
    }
  },
  'metadata': {
    'spec_version': 1,
    'name': endpoint_name,
    'kind': 'endpoint',
    'project_reference': {
      'kind': 'project',
      'uuid': project_uuid,
      'name': project_name
    }
  },
  'api_version': '3.0'
}

# add powershell protocol type for windows OS
if endpoint_type == 'Windows':
    payload['spec']['resources']['attrs']['connection_protocol'] = 'http'

r = requests.post(url.format('endpoints/import_json'), json=payload, **kwargs)
if r.status_code == 200:
    endpoint_uuid = r.json()['metadata']['uuid']
    print('INFO - endpoint created with uuid: {}'.format(endpoint_uuid))
else:
    print('ERROR - endpoint creation failed, statuc code: {}, message: {}'.format(r.status_code, r.content))
    exit(0)

# add credentials to endpoint
r = requests.get(url.format('endpoints/'+endpoint_uuid), **kwargs)
payload = r.json()

del payload['status']
payload['spec']['resources']['attrs']['credential_definition_list'][0]['secret']['value'] = endpoint_password
payload['spec']['resources']['attrs']['credential_definition_list'][0]['secret']['attrs']['is_secret_modified'] = True

r = requests.put(url.format('endpoints/'+endpoint_uuid), json=payload, **kwargs)
if r.status_code == 200:
    print('INFO - Endpoint secret updated')
    print('ENDPOINT_UUID={}'.format(endpoint_uuid))
else:
    print('ERROR - secret update failed, status code: P{}, message: {}'.format(r.status_code, r.content))