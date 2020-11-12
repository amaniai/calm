from calm.dsl.builtins import read_local_file, basic_cred

# Change values based on your calm environment
NETWORK_NAME = 'Network-01'
VM_USERNAME = 'nutanix'

# Secret variables (.local file store)
ERA_PASSWORD_VALUE = read_local_file('era')
DB_PASSWORD_VALUE = read_local_file('db_password')
CENTOS_KEY = read_local_file('centos')


# Blueprint credentials
ERA_CRED = basic_cred('admin', ERA_PASSWORD_VALUE, name='ERA_CRED', type='PASSWORD')
CENTOS_CRED = basic_cred(VM_USERNAME, CENTOS_KEY, name='CENTOS_CRED', type='KEY', default=True)
