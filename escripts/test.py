

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
    # policy, status = http_request('network_security_rules/{}'.format(policy_uuid), method='GET')

    if True:
        acl = []
        for ace in current_acl:
            acl.append(generate_ace(ace))
        
        acl.append(generate_ace(new_ace))
        print(acl)

        # del(policy['status'])
        # policy['spec']['resources']['app_rule']['inbound_allow_list'] = acl
    #     _, ok = http_request('network_security_rules/{}'.format(policy_uuid), payload=policy_uuid, method='PUT')
    #     if ok:
    #         print('API for policy updated passed ...')
    #         return acl, True
    #     else:
    #         print('Error in API call to update policy')
    #         return None, False
    # else:
    #     print('Error not able to get current policy')
    #     return None, False


# ##########################################################################################
# Main task function
# ##########################################################################################

policy_uuid = '23423423'
if len('') == 0:
    current_acl = []
else:
    current_acl = json.loads('{}')

ace = {
    'ip': '1.1.1.0',
    'prefix': int('24'),
    'protocol': 'ICMP',
    'port': int('0')
}

# new_acl, status = append_security_policy(policy_uuid, current_acl, ace)
append_security_policy(policy_uuid, current_acl, ace)
# if status:
#     print('Policy updated ...')
#     print('INBOUND_ACL={}'.format(json.dumps(new_acl)))
# else:
#     print('Error in updating the policy')

