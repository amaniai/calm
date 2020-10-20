# Task name: create a new network for the tenant
# Description:  Creates a vlan on PC and adds it to the tenant project
# Type: set variable
# Required input: VLAN_ID, CLUSTER_UUID, VPC_NAME, CATEGORY_NAME
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

vlan_id = int('@@{VLAN_ID}@@')
cluster_uuid = '@@{CLUSTER_UUID}@@'
network_name = '@@{calm_application_name}@@'
bridge_name = 'br0'
category_name = 'network_owner'
project_name = '@@{calm_project_name}@@'
ip_subnet = '@@{IP_SUBNET}@@'
default_gateway = ip_subnet[:ip_subnet.rfind('.')]+'.1'
network_prefix = int('@@{NETWORK_PREFIX}@@')
enable_dhcp = '@@{ENABLE_DHCP}@@'.lower() == 'yes'
dns_servers = '@@{DNS_SERVERS}@@'.replace(' ', '').split(',')
domain_name = '@@{DOMAIN_NAME}@@'
pool_start = ip_subnet[:ip_subnet.rfind('.')]+'.100'
pool_end = ip_subnet[:ip_subnet.rfind('.')]+'.200'


payload = {
    'spec': {
        'name': network_name,
        'resources': {
            'vswitch_name': bridge_name,
            'subnet_type': 'VLAN',
            'vlan_id': vlan_id,
            'ip_config': {
                'default_gateway_ip': default_gateway,
                'subnet_ip': ip_subnet,
                'prefix_length': network_prefix
            }
        },
        'cluster_reference': {'kind': 'cluster', 'uuid': cluster_uuid}
    },
    'api_version': '3.1',
    'metadata': {
        'kind': 'subnet',
        'categories_mapping': {category_name: [project_name]},
        'use_categories_mapping': True
    }
}
if enable_dhcp:
    payload['spec']['resources']['ip_config']['dhcp_options'] = \
        {'domain_name': domain_name,
        'domain_search_list': [domain_name],
        'domain_name_server_list': dns_servers}
    payload['spec']['resources']['ip_config']['pool_list'] = [{'range': '{} {}'.format(pool_start,pool_end)}]

url = '{}/subnets'.format(base_url)

resp = requests.post(url, json=payload, **kwargs)
if resp.status_code == 202:
    print('Network create call ok')
    network_uuid = resp.json()['metadata']['uuid']
    print('NETWORK_UUID={}'.format(network_uuid))
else:
    print('Error while calling network create, status code: {}'.format(resp.status_code))
    print(resp.content)
    exit(1)

