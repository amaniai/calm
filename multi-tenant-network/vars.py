from calm.dsl.builtins import read_local_file, basic_cred

# Change values based on your calm environment
ARISTA_ENDPOINT = '10.0.0.1'


# Secret variables (.local file store)
PC_PASSWORSD = read_local_file('prism_central')
ARISTA_PASSWORD = read_local_file('arista')

# Blueprint credentials
PC_CRED = basic_cred('admin', PC_PASSWORSD, name='PC_CRED', type='PASSWORD')
ARISTA_CRED = basic_cred('admin', ARISTA_PASSWORD, name='ARSITA_CRED', type='PASSWORD', default=True)
