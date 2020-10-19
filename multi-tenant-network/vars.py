from calm.dsl.builtins import read_local_file, basic_cred

# Change values based on your calm environment
ARISTA_ENDPOINT = '10.0.0.1'


# Secret variables (.local file store)
ARISTA_PASSWORD = read_local_file('arista')

# Blueprint credentials
ARISTA_CRED = basic_cred('admin', ARISTA_PASSWORD, name='ARSITA_CRED', type='PASSWORD', default=True)
