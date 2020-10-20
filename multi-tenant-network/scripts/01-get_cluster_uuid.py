# Task name: get the target cluster uuid from name
# Description:
# Type: set variable
# Required input: CLUSTER_NAME
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
# cluster_name = 'DC-1'
# kwargs = {'verify': False, 'headers': {'Authorization': 'Bearer {}'.format('@@{calm_jwt}@@')}}
kwargs = {'verify': False, 'auth': ('@@{PC_CRED.username}@@', '@@{PC_CRED.secret}@@')}
base_url = 'https://127.0.0.1:9440/api/nutanix/v3'
cluster_name = '@@{CLUSTER_NAME}@@'

url = '{}/clusters/list'.format(base_url)
payload = {'kind': 'cluster', 'length': 9999}
resp = requests.post(url, json=payload, **kwargs)
if resp.status_code == 200:
    for cluster in resp.json()['entities']:
        if cluster['spec']['name'] == cluster_name:
            print('CLUSTER_UUID={}'.format(cluster['metadata']['uuid']))
            exit(0)
else:
    print('Error in getting cluster name, status code: {}'.format(resp.status_code))
    print(resp.content)
    exit(1)
