import json

current_acl = json.loads('[{"ip": "0.0.0.0", "prefix": 0, "protocol": "TCP", "port": 22}, {"ip": "0.0.0.0", "prefix": 0, "protocol": "TCP", "port": 5985}, {"ip": "0.0.0.0", "prefix": 0, "protocol": "ICMP", "port": 0}]')

if len('@@{INBOUND_ACL}@@') == 0 or '@@{INBOUND_ACL}@@' == 'null':
    current_acl = []
else:
    current_acl = json.loads('@@{INBOUND_ACL}@@')

print("No\t Source\t\t Protocol")
print("=====================================")
for index, ace in enumerate(current_acl):
    if ace['protocol'] == 'TCP' or ace['protocol'] == 'UDP':
        print('[{}]\t {}/{}\t {}/{}'.format(index, ace['ip'], ace['prefix'], 
        ace['port'], ace['protocol'].lower()))
    else:
        print('[{}]\t {}/{}\t {}'.format(index, ace['ip'], ace['prefix'], 
        ace['protocol'].lower()))

