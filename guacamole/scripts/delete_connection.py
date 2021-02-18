import requests

# -------------- Test Environment ------------------
# import urllib3
# urllib3.disable_warnings()
#
# base_url = 'https://lab.ntnx.me/access/api/'
# api_username = 'guacadmin'
# api_password = 'NTNX/4u2020'
#
# access_username = 'hussain'
# connection_id = '6'

# -------------- Calm Environment ------------------
base_url = '@@{ACCESS_URL}@@'
api_username = '@@{GUACADMIN.username}@@'
api_password = '@@{GUACADMIN.secret}@@'

access_username = '@@{ACCESS_USERNAME}@@'
connection_id = '@@{CONNECTION_ID}@@'


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

# delete the connection
# ---------------------------------------
url = base_url + 'session/data/{}/connections/{}?token={}'.format(data_source, connection_id, auth_token)
resp = requests.delete(url)
if resp.status_code == 204:
    print('INFO - connection {} deleted successfully'.format(connection_id))
else:
    print('ERROR - connection delete failed, status code: {}, msg: {}'.format(resp.status_code, resp.content))
    exit(1)


# check if user has any other connections
# ---------------------------------------------------------------------------
url = base_url + 'session/data/{}/users/{}/permissions?token={}'.format(data_source, access_username, auth_token)
resp = requests.get(url, json={})
if len(resp.json().get('connectionPermissions', {})) == 0:
    print('INFO - User has no more connections, deleting the user account')
    url = base_url + 'session/data/{}/users/{}?token={}'.format(data_source, access_username, auth_token)
    resp = requests.delete(url)
    if resp.status_code == 204:
        print('INFO - user {} deleted successfully'.format(access_username))
    else:
        print('ERROR - user delete failed, status code: {}, msg: {}'.format(resp.status_code, resp.content))
        exit(1)
else:
    print('INFO - user {} has still more connections assigned'.format(access_username))

