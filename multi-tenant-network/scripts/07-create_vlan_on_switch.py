# Task name: create vlan on switch
# Description:  Create the vlan with name on the arista switch
# Type: set variable
# Required input: VLAN_ID
#
# Version: v1.0
# Author: Husain Ebrahim <husain.ebrahim@nutanix.com>


import requests
# from pprint import pprint
# import json
# import urllib3
# urllib3.disable_warnings()

arista_ip = '@@{ARISTA_IP}@@'
vlan_id = '@@{VLAN_ID}@@'
vlan_name = '@@{calm_application_name}@@'

url = 'http://{}/command-api'.format(arista_ip)
kwargs = {'verify': False, 'auth': ('@@{ARISTA_CRED.username}@@', '@@{ARISTA_CRED.secret}@@')}

payload = {
    'jsonrpc': '2.0',
    'method': 'runCmds',
    'params': {
        'version': 1,
        'cmds': [
            'enable',
            'configure',
            'vlan {}'.format(vlan_id),
            'name {}'.format(vlan_name)
        ],
        'format': 'json'
    },
    'id': 'CalmAPI'
}
resp = requests.post(url, json=payload, **kwargs)
if resp.status_code == 200:
    print('VLAN {} created successfully on the switch'.format(vlan_name))
else:
    print('Error while creating vlan on the switch, status code: {}'.format(resp.status_code))
    print(resp.content)
    exit(1)
