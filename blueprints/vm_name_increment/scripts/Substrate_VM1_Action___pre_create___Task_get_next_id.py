import requests

# -------------- Test Environment ------------------
# import urllib3
# urllib3.disable_warnings()
# authorization = 'Basic YWRtaW46bngyVGVjaDkxMSE='
# url = 'https://10.38.17.73:9440/api/nutanix/v3/{}'
# project_name = 'default'
# app_type = 'WWW'


# -------------- Calm Environment ------------------
vm_uuid = "@@{id}@@"
authorization = 'Bearer @@{calm_jwt}@@'
url = 'https://127.0.0.1:9440/api/nutanix/v3/{}'
project_name = '@@{calm_project_name}@@'
app_type = '@@{APP_TYPE}@@'


kwargs = {
    'verify': False,
    'headers': {'Authorization': authorization}
}


# ----------------- search for VM names starting with Project_name+App_type -----------------
payload = {
    'kind': 'vm',
    'filter': 'vm_name=={}.*'.format(project_name+app_type),
    'sort_order': 'DESCENDING',
    'sort_attribute': 'vm_name'
}
resp = requests.post(url.format('vms/list'), json=payload, **kwargs)
if resp.status_code == 200:
    vm_list = resp.json()['entities']
    print('INFO - Prism has: {} vms starting with {}'.format(len(vm_list), project_name+app_type))
    if len(vm_list):
        try:
            vm_name = vm_list[0]['spec']['name']
            current_count = int(vm_list[0]['spec']['name'][-3:])
            print('INFO - last vm unique count: {}'.format(current_count))
            print('VM_ID={0:0=3d}'.format(current_count + 1))
            exit(0)
        except Exception as error:
            print('ERROR - Last VM name does not match the expected pattern, vm name: {}'.format(vm_name))
            print('ERROR - msg:{}'.format(error))
else:
    print('ERROR - get vm api call failed, status code: {}'.format(resp.status_code))
    print('ERROR - Msg: {}'.format(resp.content))

print('INFO - not able to get latest vm count, failing back to 001')
print('VM_ID=001')

