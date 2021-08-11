# Name: get email of user from AD
# Task Type: set variable
# Script Type: EScript
# Author: Husain Ebrahim <husain.ebrahim@nutanix.com>
# Date: 11-08-2021
# Description:

import requests

# General script settings
# --------------------------------------------------
email = 'husain@dc1.demo'
subject = 'Hello from escript'
body = 'Hello body'
webhook_id = 'f29132be-9c0d-4091-b3c4-61f172f018bb'

# -------------- Test Environment ------------------
import urllib3
urllib3.disable_warnings()
authorization = 'Basic xxxx'
url = 'https://10.38.11.9:9440/api/nutanix/v3/{}'

# -------------- Calm Environment ------------------
# authorization = 'Bearer @@{calm_jwt}@@'
# url = 'https://127.0.0.1:9440/api/nutanix/v3/{}'

kwargs = {
    'verify': False,
    'headers': {'Authorization': authorization}
}

payload = {
    'trigger_type': 'incoming_webhook_trigger',
    'trigger_instance_list': [{
        'webhook_id': webhook_id,
        'string1': email,
        'string2': subject,
        'string3': body
    }]
}

r = requests.post(url.format('action_rules/trigger'), json=payload, **kwargs)
print('Email api status code: {}, result: {}'.format(r.status_code, r.content))