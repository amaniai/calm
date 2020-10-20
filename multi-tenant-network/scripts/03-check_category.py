# Task name: check category
# Description:  Check if category exists, else it will create it
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

url = '{}/categories/list'.format(base_url)
payload = {'filter': 'name=={}'.format(category_name), 'kind': 'category', 'length': 9999}
resp = requests.post(url, json=payload, **kwargs)
if resp.status_code == 200 and len(resp.json()['entities']):
    print('category name found')
else:
    print('category not found, creating one')
    url = '{}/categories/{}'.format(base_url, category_name)
    payload = {
        'name': category_name,
        'description': 'category to label network owners created by Calm multi-tenant network'
    }
    resp = requests.put(url, json=payload, **kwargs)
    if resp.status_code == 200:
        print('category created successfully, uuid: {}'.format(category_name))
    else:
        print('Error while creating category, status code: {}'.format(resp.status_code))
        print(resp.content)
        exit(1)

