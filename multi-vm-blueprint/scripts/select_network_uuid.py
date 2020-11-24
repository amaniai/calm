import requests

# General script settings
# --------------------------------------------------
category_key = 'network'
category_value_yes = 'external'
category_value_no = 'internal'

# -------------- Test Environment ------------------
# import json
# import urllib3
# urllib3.disable_warnings()
# user_network_answer = 'yes'
# project_name = 'test'
# authorization = 'Basic YWRtaW46bngyVGVjaDkxMSE='
# url = 'https://10.38.2.9:9440/api/nutanix/v3/{}'

# -------------- Calm Environment ------------------
user_network_answer = '@@{INTERNET_ACCESS}@@'.lower()
project_name = '@@{calm_project_name}@@'
authorization = 'Bearer @@{calm_jwt}@@'
url = 'https://127.0.0.1:9440/api/nutanix/v3/{}'


kwargs = {
    'verify': False,
    'headers': {'Authorization': authorization}
}


# --------- Get project details (networks, limits and usage) -------------------
# ------------------------------------------------------------------------------
payload = {'kind': 'project'}
resp = requests.post(url.format('projects/list'), json=payload, **kwargs)
project_networks = []
project_limits = {}
project_usage = {}
if resp.status_code == 200:
    for project in resp.json()['entities']:
        if project['spec']['name'] == project_name:
            print('INFO - Found project {} with uuid: {}'.format(project_name, project['metadata']['uuid']))
            project_networks = project['spec']['resources']['subnet_reference_list']
else:
    print('ERROR - Projects list API call failed, status code: {}'.format(resp.status_code))
    print('ERROR - Msg: {}'.format(resp.content))
    exit(1)


# ------------ get network categories (external or internal) -------------------
# ------------------------------------------------------------------------------
payload = {'kind': 'subnet'}
resp = requests.post(url.format('subnets/list'), json=payload, **kwargs)
all_networks = {}
if resp.status_code == 200:
    # loop through project networks and match categories
    for network in resp.json()['entities']:
        all_networks[network['metadata']['uuid']] = network['metadata']['categories']
else:
    print('ERROR - subnet list api called failed, status code: {}'.format(resp.status_code))
    print('ERROR - Msg: {}'.format(resp.content))
    exit(1)


# --------------------- set the vm network ----------------------------------
# ---------------------------------------------------------------------------
vm_network = {}
if user_network_answer == 'yes':
    category_value = category_value_yes
else:
    category_value = category_value_no
for network in project_networks:
    if all_networks[network['uuid']].get(category_key) == category_value:
        vm_network = network
        print('INFO - found the required network: {}, with category: {}:{}'
              .format(network['name'], category_key, category_value))

print('VM_NETWORKK={}'.format(json.dumps(vm_network)))
