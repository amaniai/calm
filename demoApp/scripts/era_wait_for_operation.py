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

operation_id = '@@{OPERATION_ID}@@'

if len(operation_id) == 0:
    print('No operation id found, existing without error')
    exit(0)

url = '{}/operations/{}'.format(base_url, operation_id)
for x in range(20):
    sleep(60)
    resp = requests.get(url, **kwargs)
    if resp.status_code == 200:
        job_percent = resp.json()['percentageComplete']
        job_status = resp.json()['status']
        print('Percentage Complete: {}'.format(job_percent))
        if job_percent == '100':
            print('Operation:{} completed successfully ...'.format(operation_id))
            break
        elif job_status != '1':
            print('Error - something went wrong with operation: {}'.format(operation_id))
            exit(1)

if job_percent != '100':
    print('Error - Operation:{} timed-out '.format(operation_id))
    exit(1)





