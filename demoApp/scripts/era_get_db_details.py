# Task name: Provision PostgreSQL on Era (single instance)
# Description:  The propose of this script is to provision Postgres DB on ERA
#
# Version: v1.0
# Author: Husain Ebrahim <husain.ebrahim@nutanix.com>

# ERA API call function
# ================================================================
import requests
# from pprint import pprint
# from time import sleep


base_url = 'https://@@{ERA_IP}@@/era/v0.9'
kwargs = {
    'verify': False,
    'auth': ('@@{ERA_CRED.username}@@', '@@{ERA_CRED.secret}@@')
}

db_name = '@@{DBSERVER_NAME}@@'

url = '{}/databases?value-type=name&value={}'.format(base_url, db_name)
resp = requests.get(url, **kwargs)
vm_ip = ''
if resp.status_code == 200:
    db = resp.json()[0]
    db_id = db['id']
    dbserver_id = db['databaseNodes'][0]['dbserverId']
    for item in db['properties']:
        if item['name'] == 'vm_ip':
            dbserver_ip = item['value']

print('DB_ID={}'.format(db_id))
print('DBSERVER_ID={}'.format(dbserver_id))
print('DBSERVER_IP={}'.format(dbserver_ip))






