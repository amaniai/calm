# Task name: era_set_credentials
# Description:  Testing the current logged in user if authorized on Era else will go with default
#
# Version: v1.0
# Author: Husain Ebrahim <husain.ebrahim@nutanix.com>

# ERA API call function
# ================================================================
import requests

username = '@@{calm_username}@@'
passwrod = '@@{ERA_CRED.secret}@@'
base_url = 'https://@@{ERA_IP}@@/era/v0.9'

kwargs = {
    'verify': False,
    'auth': (username, passwrod)
}

url = '{}/clusters'.format(base_url)
resp = requests.get(url, **kwargs)
if resp.status_code == 200:
    print('ERA_USERNAME={}'.format(username))
    print('ERA_PASSWORD={}'.format(passwrod))
else:
    print('ERA_USERNAME={}'.format('@@{ERA_CRED.username}@@'))
    print('ERA_PASSWORD={}'.format('@@{ERA_CRED.secret}@@'))
