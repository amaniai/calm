# Name: Generate Generate next avialable project code, format P001
# Task Type: set variable
# Script Type: EScript
# Author: Husain Ebrahim <husain.ebrahim@nutanix.com>
# Date: 25-09-2021
# Description:

import requests

# -------------- General settings ------------------
CODE_PREFIX = 'P'
COUNT_DIGITS = 3


# -------------- Test Environment ------------------
import urllib3
urllib3.disable_warnings()
authorization = 'Basic YWRtaW46bngyVGVjaDkxMSE='
url = 'https://10.38.12.9:9440/api/nutanix/v3/{}'
project_category = 'PROJECTS'

# -------------- Calm Environment ------------------
# authorization = 'Bearer @@{calm_jwt}@@'
# url = 'https://127.0.0.1:9440/api/nutanix/v3/{}'
# project_category = '@@{PROJECT_CATEGORY}@@'

kwargs = {
    'verify': False,
    'headers': {'Authorization': authorization}
}

payload = {'kind': 'category'}
r = requests.post(url.format('categories/'+project_category+'/list'), json=payload, **kwargs)
project_code = ''

if r .status_code == 200:
    current_count = int(r.json()['metadata']['total_matches'])
    print('INFO - current project code count: {}'.format(current_count))
    
    digit_format = '{'+'0:0={}d'.format(COUNT_DIGITS)+'}'
    next_count = digit_format.format(current_count+1)
    project_code = '{}{}'.format(CODE_PREFIX, next_count)
    print('INFO - adding {} to category'.format(project_code))

# if the category key doesn't exist then create it
if current_count == 0:
    payload = {'name': project_category}
    print('INFO - category key is not available, creating it')
    r = requests.put(url.format('categories/'+project_category), json=payload, **kwargs)
    print('INFO - creating category status code: {}'.format(r.status_code))

# adding the new project code to the category
payload = {'value': project_code}
r = requests.put(url.format('categories/'+project_category+'/'+project_code), json=payload, **kwargs)

print('PROJECT_CODE={}'.format(project_code))
