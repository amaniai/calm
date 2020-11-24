import requests
import urllib3
urllib3.disable_warnings()


project_name = 'default'
# project_name = '@@{calm_project_name}@@'

authorization = 'Basic YWRtaW46TlROWC80dTIwMTk='
# authorization = 'Bearer @@{calm_jwt}@@'

url = 'https://10.0.0.98:9440/api/nutanix/v3/{}'
# url = 'https://127.0.0.1:9440/api/nutanix/v3/{}'
kwargs = {
    'verify': False,
    'headers': {'Authorization': authorization}
}


payload = {'kind': 'project'}
resp = requests.post(url.format('projects/list'), json=payload, **kwargs)
networks = []
if resp.status_code == 200:
    for project in resp.json()['entities']:
        if project['spec']['name'] == project_name:
            print('INFO - Found project {} with uuid: {}'.format(project_name, project['metadata']['uuid']))
            networks = project['spec']['resources']['subnet_reference_list']
else:
    print('ERROR - Porject list API call failed, status code: {}'.format(resp.status_code))
    print('ERROR - Msg: {}'.format(resp.content))

print(networks)