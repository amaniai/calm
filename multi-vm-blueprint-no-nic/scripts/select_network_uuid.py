import requests

# -------------- Test Environment ------------------
# import json
# import urllib3
# urllib3.disable_warnings()
# user_network_answer = 'yes'
# project_name = 'default'
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

if user_network_answer.lower() == 'no':
    print('INFO - no network access, stopping script')
    exit(0)
# --------- Get project details (networks, limits and usage) -------------------
# ------------------------------------------------------------------------------
payload = {'kind': 'project'}
resp = requests.post(url.format('projects/list'), json=payload, **kwargs)
vm_network = {}
if resp.status_code == 200:
    for project in resp.json()['entities']:
        if project['spec']['name'] == project_name:
            print('INFO - Found project {} with uuid: {}'.format(project_name, project['metadata']['uuid']))
            if project['status']['resources']['is_default']:
                vm_network = project['status']['resources']['default_subnet_reference']
                print('INFO - selecting project default network: {}'.format(vm_network))
            else:
                vm_network = project['status']['resources']['subnet_reference_list'][0]
                print('WARNING - no default network is set on the project, returning first network: {}'
                      .format(vm_network))
            print('VM_NETWORK={}'.format(json.dumps(vm_network)))
            exit(0)
else:
    print('ERROR - Projects list API call failed, status code: {}'.format(resp.status_code))
    print('ERROR - Msg: {}'.format(resp.content))
    exit(1)

