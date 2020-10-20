# Task name: update_project_network
# Description:  update current project with the new network
# Type: set variable
# Required input: NETWORK_UUID, CLUSTER_UUID
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

network_uuid = '@@{NETWORK_UUID}@@'
project_name = '@@{calm_project_name}@@'

url = '{}/projects/list'.format(base_url)
payload = {'kind': 'project', 'filter': 'name=={}'.format(project_name), 'length': 9999}
resp = requests.post(url, json=payload, **kwargs)
if resp.status_code == 200 and len(resp.json()['entities']):
    payload = resp.json()['entities'][0]
    payload.pop('status')
    payload['spec']['resources']['subnet_reference_list'].append(
        {'kind': 'subnet', 'uuid': network_uuid}
    )
    url = '{}/projects/{}'.format(base_url, payload['metadata']['uuid'])
    resp = requests.put(url, json=payload, **kwargs)
    if resp.status_code == 202:
        print('Network added to the tenant project successfully ...')
    else:
        print('Error while updating tenant project, status code: {}'.format(resp.status_code))
        print(resp.content)
        exit(1)
else:
    print('Error getting the project details, status code: {}'.format(resp.status_code))
    print(resp.content)
    exit(1)
