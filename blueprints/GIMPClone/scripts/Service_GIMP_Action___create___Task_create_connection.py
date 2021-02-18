import requests

# -------------- Test Environment ------------------
# import urllib3
# urllib3.disable_warnings()

# base_url = 'https://lab.ntnx.me/access/api/'
# api_username = 'guacadmin'
# api_password = 'NTNX/4u2020'

# access_username = 'hussain'
# access_password = 'nutanix/4u'
# vm_name = 'Windows DC4'
# vm_ip = '10.0.0.118'
# vm_port = '3389'
# vm_username = 'administrator'
# vm_password = 'NTNX/4u2019'
# remote_app = '||GIMP'

# -------------- Calm Environment ------------------
base_url = '@@{ACCESS_URL}@@'
api_username = '@@{GUACADMIN.username}@@'
api_password = '@@{GUACADMIN.secret}@@'

access_username = '@@{ACCESS_USERNAME}@@'
access_password = '@@{ACCESS_PASSWORD}@@'
vm_name = '@@{calm_project_name}@@-@@{calm_application_name}@@-@@{calm_array_index}@@-GIMP'
vm_ip = '@@{address}@@'
vm_port = '3389'
vm_username = 'administrator'
vm_password = '@@{ADMIN_PASS}@@'
remote_app = '@@{REMOTE_APP}@@'


# Authenticate with username and password to get authentication token
# ----------------------------------------------------------------------------
kwargs = {
    'verify': False,
    'headers': {'Content-Type': 'application/x-www-form-urlencoded'}
}
authen_payload = 'username={}&password={}'.format(api_username, api_password)
url = base_url + 'tokens'
resp = requests.post(url, data=authen_payload, **kwargs)
if resp.status_code == 200:
    print('INFO - successfully authenticated with Guacamole')
    auth_token = resp.json()['authToken']
    data_source = resp.json()['dataSource']
    kwargs['headers']['Content-Type'] = 'application/json'
else:
    print('ERROR - authentication failed, status code: {}, msg: {}'.format(resp.status_code, resp.content))
    exit(1)

# verify if the user already created
url = base_url + 'session/data/{}/users?token={}'.format(data_source, auth_token)
resp = requests.get(url, **kwargs)
if resp.status_code == 200:
    print('INFO - user list fetched')
    if access_username not in resp.json():
        print('INFO - user not found, creating the user')
        payload = {'username': access_username, 'password': access_password,'attributes': {}}
        resp = requests.post(url, json=payload, **kwargs)
        if resp.status_code == 200:
            print('INFO - user created successfully...')
        else:
            print('ERROR - User creation failed, status code: {}, msg: {}'.format(resp.status_code, resp.content))
else:
    print('ERROR - fetching users failed, status code: {}, msg: {}'.format(resp.status_code, resp.content))
    exit(1)


# Create RDP connection
# ----------------------------------------------
payload = {
    'parentIdentifier': 'ROOT',
    'name': vm_name,
    'protocol': 'rdp',
    'attributes': {},
    'parameters': {
        'port': vm_port,
        'ignore-cert': True,
        'hostname': vm_ip,
        'username': vm_username,
        'password': vm_password,
        'remote-app': remote_app
    }
}
url = base_url + 'session/data/{}/connections?token={}'.format(data_source, auth_token)
resp = requests.post(url, json=payload, **kwargs)
if resp.status_code == 200:
    connection_id = resp.json()['identifier']
    print('INFO - connection created successfully for VM: {}'.format(vm_name))
    print('INFO - new connection identifier: {}'.format(connection_id))
else:
    print('ERROR - connection creation failed, status code: {}, msg: {}'.format(resp.status_code, resp.content))
    exit(1)


# Update user with connection permission
# --------------------------------------------------------------------------------
url = base_url + 'session/data/{}/users/{}/permissions?token={}'.format(data_source, access_username, auth_token)
payload = [{'op': 'add', 'path': '/connectionPermissions/{}'.format(connection_id), 'value': 'READ'}]
resp = requests.patch(url, json=payload, **kwargs)
if resp.status_code == 204:
    print('INFO - connection assigned to user')
else:
    print('ERROR - failed to assign connection to user, status code: {}, msg: {}'.format(resp.status_code, resp.content))
    exit(1)

# print info
print('CONNECTION_ID={}'.format(connection_id))

