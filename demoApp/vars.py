from calm.dsl.builtins import read_local_file, basic_cred

# Change values based on your calm environment
IMAGE_NAME = 'centos-7'
NETWORK_NAME = 'Network-1'
VM_USERNAME = 'nutanix'


# Secret variables (.local file store)
CENTOS_KEY = read_local_file('centos')
ERA_PASSWORD_VALUE = read_local_file('era')
DB_PASSWORD_VALUE = read_local_file('db_password')

# Blueprint credentials
CENTOS_CRED = basic_cred(VM_USERNAME, CENTOS_KEY, name='CENTOS_CRED', type='KEY', default=True)
ERA_CRED = basic_cred('admin', ERA_PASSWORD_VALUE, name='ERA_CRED', type='PASSWORD')
