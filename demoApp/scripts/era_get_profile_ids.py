# Task name: get profile detials of Era DB
# Description:  The propose of this script is to provision Postgres DB on ERA
#
# Version: v1.0
# Author: Husain Ebrahim <husain.ebrahim@nutanix.com>

# ERA API call function
# ================================================================
import requests


def get_cluster_id (name=''):
    url = '{}/clusters'.format(base_url)
    resp = requests.get(url, **kwargs)
    if resp.status_code == 200:
        return resp.json()[0]['id']


def get_all_parameters(profiles):
    url = '{}/profiles'.format(base_url)
    resp = requests.get(url, **kwargs)
    if resp.status_code == 200:
        for profile in resp.json():
            if profile['topology'] == 'ALL' or profile['topology'] == 'single':
                if profile['engineType'] == 'Generic' or profile['engineType'] == 'postgres_database':
                    profiles[profile['type'].lower()] = {'id': profile['id'],
                                                         'name': profile['name'],
                                                         'version': profile['versions'][0]['id']}

    return profiles


def get_sla_id(sla_name='NONE'):
    url = '{}/slas'.format(base_url)
    resp = requests.get(url, **kwargs)

    if resp.status_code:
        for sla in resp.json():
            if sla['name'] == sla_name:
                return sla['id']

# ##########################################################################################
# Main task function
# ##########################################################################################

base_url = 'https://@@{ERA_IP}@@/era/v0.9'
kwargs = {
    'verify': False,
    'auth': ('@@{ERA_CRED.username}@@', '@@{ERA_CRED.secret}@@')
}
profiles = {
    'software': {'name': '@@{SOFTWARE_PROFILE}@@', 'id': ''},
    'compute': {'name': '@@{COMPUTE_PROFILE}@@', 'id': ''},
    'network': {'name': '@@{NETWORK_PROFILE}@@', 'id': ''},
    'database_parameter': {'name': '@@{DATABASE_PARAMETER}@@', 'id': ''}
}

db_name = '@@{DB_NAME}@@'

cluster_id = get_cluster_id()
profiles = get_all_parameters(profiles)
sla_id = get_sla_id()

print('CLUSTER_ID={}'.format(cluster_id))
print('SOFTWARE_ID={}'.format(profiles['software']['id']))
print('SOFTWARE_VERSION={}'.format(profiles['software']['version']))
print('COMPUTE_ID={}'.format(profiles['compute']['id']))
print('NETWORK_ID={}'.format(profiles['network']['id']))
print('DB_PARAMETER={}'.format(profiles['database_parameter']['id']))
print('SLA_ID={}'.format(sla_id))

