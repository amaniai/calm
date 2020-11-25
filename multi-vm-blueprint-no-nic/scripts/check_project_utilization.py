import requests

# -------------- Test Environment ------------------
# import urllib3
# urllib3.disable_warnings()
# project_name = 'test'
# authorization = 'Basic YWRtaW46bngyVGVjaDkxMSE='
# url = 'https://10.38.2.9:9440/api/nutanix/v3/{}'
# vcpu = 1
# memory = 4
# disk_size = 100
# index = 0
# count = 2

# -------------- Calm Environment ------------------
project_name = '@@{calm_project_name}@@'
authorization = 'Bearer @@{calm_jwt}@@'
url = 'https://127.0.0.1:9440/api/nutanix/v3/{}'
vcpu = int('@@{cpunum}@@')
memory = int('@@{memorynum}@@')
disk_size = int('@@{storage}@@')
index = int('@@{calm_array_index}@@')
count = int('@@{count}@@')

kwargs = {
    'verify': False,
    'headers': {'Authorization': authorization}
}

# exit if running on the first instance
if index:
    print('INFO - will only run on the first instance')
    exit(0)

# --------- Get project details (networks, limits and usage) -------------------
# ------------------------------------------------------------------------------
payload = {'kind': 'project'}
project_limits = {}
project_uuid = ''
resp = requests.post(url.format('projects/list'), json=payload, **kwargs)
if resp.status_code == 200:
    for project in resp.json()['entities']:
        if project['spec']['name'] == project_name:
            project_uuid = project['metadata']['uuid']
            print('INFO - uuid for project ({}) is: {}'.format(project_name, project_uuid))
            if project['spec']['resources'].get('resource_domain'):
                for resource in project['spec']['resources']['resource_domain']['resources']:
                    project_limits[resource['resource_type'].lower()] = resource['limit']
                print('INFO - found project limits: {}'.format(project_limits))
            else:
                print('INFO - No project limits, stopping check')
                exit(0)


# --------- Get project utilization  ----------------------- -------------------
# ------------------------------------------------------------------------------
payload = {
    "entity_type": "vm",
    "group_member_sort_attribute": "memory_size_bytes",
    "group_member_sort_order": "DESCENDING",
    "group_member_attributes": [
        {"attribute": "memory_size_bytes"},
        {"attribute": "capacity_bytes"},
        {"attribute": "project_name"},
        {"attribute": "num_vcpus"}
    ],
    "query_name": "prism:BaseGroupModel",
    "availability_zone_scope": "GLOBAL",
    "filter_criteria": "project_reference=in={}".format(project_uuid),
    "group_member_offset": 0,
    "group_member_count": 1000
}
#
resp = requests.post(url.format('groups'), json=payload, **kwargs)
project_usage = {'vcpus': 0, 'memory': 0, 'storage': 0}

if resp.status_code == 200:
    if resp.json().get('filtered_entity_count'):
        result = resp.json()['group_results'][0].get('entity_results', [])
        print(resp.json())
        for resource in result:
            remapped = {}
            for item in resource.get('data'):
                if item['values']:
                    remapped[item['name']] = item['values'][0]['values'][0]

            project_usage['vcpus'] += int(remapped.get('num_vcpus', 0))
            project_usage['memory'] += int(remapped.get('memory_size_bytes', 0))
            project_usage['storage'] += int(remapped.get('capacity_bytes', 0))

    print('INFO - Limits: {}'.format(project_limits))
    print('INFO - Usage: {}'.format(project_usage))
else:
    print('ERROR - Projects list API call failed, status code: {}'.format(resp.status_code))
    print('ERROR - Msg: {}'.format(resp.content))
    exit(1)

# check if all required resources within limits
total_vcpu = vcpu*count
total_memory = memory*count*1073741824
total_storage = disk_size*count*1073741824

if project_usage['vcpus'] + total_vcpu > project_limits['vcpus']:
    print('ERROR - CPU exceed project limit: {}'.format(project_limits['vcpus']))
    exit(1)
elif project_usage['memory'] + total_memory > project_limits['memory']:
    print('ERROR - Memory exceed project limit: {}'.format(project_limits['memory']))
    exit(1)
elif project_usage['storage'] + total_storage > project_limits['storage']:
    print('ERROR - Storage exceeds project limits: {}'.format(project_limits['storage']))
    exit(1)
else:
    print('INFO - Total resources within project limit')
    print('INFO - Total required resources: vCPU: {}, RAM: {} Bytes, Disk: {} Bytes'
          .format(total_vcpu, total_memory, total_storage))


