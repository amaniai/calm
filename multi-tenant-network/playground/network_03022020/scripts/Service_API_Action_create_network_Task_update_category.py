# api call function
# ================================================================
def http_request(api_endpoint, payload='', method='POST'):
  username = '@@{PC_ADMIN.username}@@'
  username_secret = '@@{PC_ADMIN.secret}@@'
  pc_address = '@@{PrismCentral.address}@@'
  pc_port = '9440'

  url = "https://{}:{}{}".format(
      pc_address,
      pc_port,
      api_endpoint
  )
  
  headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json'
  }
  
  if len(payload) > 0:
      payload = json.dumps(payload)
      
  
  resp = urlreq(
      url,
      verb=method,
      auth='BASIC',
      user=username,
      passwd=username_secret,
      params=payload,
      headers=headers,
      verify=False
  )
  
  if resp.ok:
      return json.loads(resp.content)
  else:
      print('Error in API call')
      exit(1)




#api_endpoint = '/api/nutanix/v3/subnets/@@{NEW_NETWORK_UUID}@@'
api_endpoint = '/api/nutanix/v3/subnets'

network = {}

network['spec'] = {'name': '@@{CUSTOMER_ID}@@-@@{NETWORK_NAME}@@'}
network['spec']['resources'] = {}
network['spec']['resources']['vswitch_name'] = '@@{BRIDGE_NAME}@@'
network['spec']['resources']['subnet_type'] = 'VLAN'
network['spec']['resources']['ip_config'] = { 'default_gateway_ip': '192.168.111.1',
                'pool_list': [{"range": "192.168.111.100 192.168.111.200"}],
                "prefix_length": 24,
                "subnet_ip": "192.168.111.0",
                "dhcp_options": {    "domain_name_server_list": '@@{DNS_SERVERS}@@'.replace(' ', '').split(','),
                                     "domain_search_list": ["demo.lan"],
                                     "domain_name": "demo.lan"}}

network['spec']['resources']['vlan_id'] = 45
network['spec']['cluster_reference'] = {'kind': 'cluster', 'uuid': '00059d94-d969-59f6-2f00-ac1f6b6911d9'}
network['api_version'] = '3.1'
network['metadata'] = {'kind': 'subnet', 'categories_mapping': {'OWNER': ['SHARED']}, 'use_categories_mapping': True}


result = http_request(api_endpoint, payload=network, method='POST')

#network = {}
#network['spec'] = result['spec']
#network['api_version'] = result['api_version']
#network['metadata'] = result['metadata']
#network['metadata']['use_categories_mapping'] = True
#del network['metadata']['last_update_time']
#del network['metadata']['creation_time']
#network['metadata']['categories_mapping']['OWNER'] = ['@@{CUSTOMER_ID}@@']

#result = http_request(api_endpoint, payload=network, method='PUT')
print(json.dumps(result))



      