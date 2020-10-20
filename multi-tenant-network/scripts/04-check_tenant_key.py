# Task name: check tenant key
# Description:  Check if key of the tenant is created on the category of network owners
# Type: set variable
# Required input: CATEGORY_NAME
#
# Version: v1.0
# Author: Husain Ebrahim <husain.ebrahim@nutanix.com>

import requests
# from pprint import pprint
# import json
# import urllib3
# urllib3.disable_warnings()


# kwargs = {'verify': False, 'auth': ('admin', 'nx2Tech911!')}
# base_url = 'https://10.38.11.9:9440/api/nutanix/v3'
kwargs = {'verify': False, 'auth': ('@@{PC_CRED.username}@@', '@@{PC_CRED.secret}@@')}
base_url = 'https://127.0.0.1:9440/api/nutanix/v3'

category_name = 'network_owner'
project_name = '@@{calm_project_name}@@'

url = '{}/categories/{}/list'.format(base_url, category_name)
payload = {'kind': 'category', 'length': 9999}
resp = requests.post(url, json=payload, **kwargs)

if resp.status_code == 200:
    for key in resp.json()['entities']:
        if key['value'] == project_name:
            print('Tenant key {} already exists in category {}'.format(project_name, category_name))
            break
    else:
        print('key {} not found in {}'.format(project_name, category_name))
        url = '{}/categories/{}/{}'.format(base_url, category_name, project_name)
        payload = {'value': project_name}
        resp = requests.put(url, json=payload, **kwargs)
        if resp.status_code == 200:
            print('Tenant key {} created successfully in {}'.format(project_name, category_name))
        else:
            print('Error while creating tenant key, status code: {}'.format(resp.status_code))
            print(resp.content)
            exit(1)
else:
    print('Error while searching for key, status code: {}'.format(resp.status_code))
    print(resp.content)
    exit(1)
