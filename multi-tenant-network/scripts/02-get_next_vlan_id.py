# Task name: get all vlans from Prism
# Description:  Get a list of configured vlans on Prism Central
# Type: set variable
# Required input: CLUSTER_UUID
#
# Version: v1.0
# Author: Husain Ebrahim <husain.ebrahim@nutanix.com>

import requests
# from pprint import pprint
# import json
# import urllib3
# urllib3.disable_warnings()


# base_url = 'https://10.38.11.9:9440/api/nutanix/v3'
# kwargs = {'verify': False, 'auth': ('admin', 'nx2Tech911!')}
# cluster_uuid = '0005b1ba-a99f-3c8e-2a27-ac1f6b1894ce'
kwargs = {'verify': False, 'auth': ('@@{PC_CRED.username}@@', '@@{PC_CRED.secret}@@')}
base_url = 'https://127.0.0.1:9440/api/nutanix/v3'
cluster_uuid = '@@{CLUSTER_UUID}@@'

vlan_ids = []
vlan_names = {}
payload = {'filter': '', 'kind': 'subnet', 'offset': 0, 'length': 9999}
url = '{}/subnets/list'.format(base_url)
resp = requests.post(url, json=payload, **kwargs)
if resp.status_code == 200:
    for vlan in resp.json()['entities']:
        if vlan['spec']['cluster_reference']['uuid'] == cluster_uuid:
            vlan_id = int(vlan['spec']['resources']['vlan_id'])
            if vlan_id not in vlan_ids:
                vlan_ids.append(vlan_id)
            vlan_names[vlan_id] = vlan['spec']['name']
    print('VLAN_IDS={}'.format(json.dumps(vlan_ids)))
    print('VLAN_NAMES={}'.format(json.dumps(vlan_names)))
else:
    print('Error in http request: {}'.format(resp.status_code))
    print(resp.content)

# usable vlan range by tenants
vlan_range_start = 1001
vlan_range_end = 1500

# check for next available vlan within range
for vlan in range(vlan_range_start, vlan_range_end):
    if vlan in vlan_ids:
        continue
    else:
        print('VLAN_ID={}'.format(vlan))
        break
