from calm.dsl.builtins import read_local_file, basic_cred

# Change values based on your calm environment
NETWORK_NAME = 'Network-01'
VM_USERNAME = 'administrator'

# Secret variables (.local file store)
ERA_PASSWORD_VALUE = read_local_file('era')
DB_PASSWORD_VALUE = read_local_file('db_password')
WINDOWS_PASSWORD_VALUE = read_local_file('windows')


# Blueprint credentials
ERA_CRED = basic_cred('admin', ERA_PASSWORD_VALUE, name='ERA_CRED', type='PASSWORD')
WINDOWS_CRED = basic_cred(VM_USERNAME, WINDOWS_PASSWORD_VALUE, name='WINDOWS_CRED', type='PASSWORD', default=True)

