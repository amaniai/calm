import json

current_acl = json.loads('[{"ip": "0.0.0.0", "prefix": 0, "protocol": "TCP", "port": 22}, {"ip": "0.0.0.0", "prefix": 0, "protocol": "TCP", "port": 5985}, {"ip": "0.0.0.0", "prefix": 0, "protocol": "ICMP", "port": 0}]')

if len(current_acl) == 0 or current_acl == 'null':
    current_acl = []
else:
    current_acl = json.loads('@@{INBOUND_ACL}@@')
drop_list = []
for index, ace in enumerate(current_acl):
    if ace['protocol'] == 'TCP' or ace['protocol'] == 'UDP':
        drop_list.append('[{}] {}/{} {}/{}'.format(index, ace['ip'], ace['prefix'], 
        ace['port'], ace['protocol'].lower()))
    else:
        drop_list.append('[{}] {}/{} {}'.format(index, ace['ip'], ace['prefix'], 
        ace['protocol'].lower()))

print(', '.join(drop_list))