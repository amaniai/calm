# Task name: get all vlans from Prism
# Description:  Get a list of configured vlans on Prism Central
# Type: set variable
#
# Version: v1.0
# Author: Husain Ebrahim <husain.ebrahim@nutanix.com>

import requests
from pprint import pprint
import json
import urllib3
urllib3.disable_warnings()


url = 'https://10.0.0.98:9440/api/nutanix/v3/subnets/list'
payload = {'filter': '', 'kind': 'subnet', 'offset': 0, 'length': 9999}
kwargs = {'verify': False, 'auth': ('admin', 'NTNX/4u2019')}
vlan_ids = []
vlan_names = {}

resp = requests.post(url, json=payload, **kwargs)
if resp.status_code == 200:
    print('List request status: {}'.format(resp.status_code))
    for vlan in resp.json()['entities']:
        vlan_id = int(vlan['spec']['resources']['vlan_id'])
        vlan_ids.append(vlan_id)
        vlan_names[vlan_id] = vlan['spec']['name']
    pprint(vlan_ids)
    pprint(vlan_names)
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
        print('TENANT_VLAN={}'.format(vlan))
        break
