#script

# Task name: Delete a security policy
# Description: Used to clean up calm-flow integeration
#
# Required Calm variables: 
#   POLICY_UUID
# Version: v1.0
# Author: Husain Ebrahim <husain.ebrahim@nutanix.com>


# Prism API call function
# ================================================================
def http_request(api_endpoint, payload='', method='POST'):
  jwt = '@@{calm_jwt}@@'
  pc_address = '127.0.0.1'
  pc_port = '9440'

  url = "https://{}:{}/api/nutanix/v3/{}".format(
    pc_address,
    pc_port,
    api_endpoint
  )

  headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer {}'.format(jwt)
  }

  if len(payload) > 0:
    payload = json.dumps(payload)


  resp = urlreq(
    url,
    verb=method,
    params=payload,
    headers=headers,
    verify=False
  )

  if resp.ok:
    return json.loads(resp.content), resp.ok
  else:
    print('Error in API call')
    print(resp)


policy_uuid = '@@{POLICY_UUID}@@'
if len(policy_uuid) != 0:
  _, status = http_request('network_security_rules/{}'.format(policy_uuid), method='DELETE')
  if status:
    print('Policy {} deleted ...'.format(policy_uuid))
  else:
    print('Error in deleting the policy')
print('POLICY_UUID=')