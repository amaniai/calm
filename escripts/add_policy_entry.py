#script

# Task name: adds a security entry to an existing flow policy
# Description: 
#
# Required Calm variables: 
#   POLICY_UUID
#   INBOUND_ACL
#   SOURCE_IP: source IP address network address
#   PREFIX: source network ID prefix
#   PROTOCOL: a list of protocol [ALL, ICMP, TCP, UDP]
#   DEST_PORT: dest port
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
      print(resp.content)


def generate_ace(ace):
    ip = ace.get('ip')
    prefix = int(ace.get('prefix', 0))
    proto = ace.get('protocol')
    port = int(ace.get('port', 0))
    entry = {
        'peer_specification_type': 'IP_SUBNET',
        'ip_subnet': {
            'ip': ip,
            'prefix_length': prefix
        },
        'protocol': proto,
    }
    
    if proto == 'TCP':
        entry['tcp_port_range_list'] = [{'start_port': port, 'end_port': port}]
    elif proto == 'UDP':
        entry['udp_port_range_list'] = [{'start_port': port, 'end_port': port}]

    return entry


def append_security_policy(policy_uuid, current_acl, new_ace):
    policy, status = http_request('network_security_rules/{}'.format(policy_uuid), method='GET')

    if status:
        acl = []
        for ace in current_acl:
            acl.append(generate_ace(ace))
        
        acl.append(generate_ace(new_ace))

        del(policy['status'])
        policy['spec']['resources']['app_rule']['inbound_allow_list'] = acl
        _, ok = http_request('network_security_rules/{}'.format(policy_uuid), payload=policy, method='PUT')
        if ok:
            print('API for policy updated passed ...')
            return True
        else:
            print('Error in API call to update policy')
            return False
    else:
        print('Error not able to get current policy')
        return False


# ##########################################################################################
# Main task function
# ##########################################################################################

policy_uuid = '@@{POLICY_UUID}@@'
if len(policy_uuid) == 0:
    print('Error: No Flow plicy loaded yet, please create one before adding entries')
    exit(1)

if len('@@{INBOUND_ACL}@@') == 0 or '@@{INBOUND_ACL}@@' == 'null':
    current_acl = []
else:
    current_acl = json.loads('@@{INBOUND_ACL}@@')

ace = {
    'ip': '@@{SOURCE_IP}@@',
    'prefix': int('0@@{PREFIX}@@'),
    'protocol': '@@{PROTOCOL}@@',
    'port': int('0@@{DEST_PORT}@@')
}

status = append_security_policy(policy_uuid, current_acl, ace)

if status:
    print('Policy updated ...')
    current_acl.append(ace)
    print('INBOUND_ACL={}'.format(json.dumps(current_acl)))
else:
    print('Error in updating the policy')

