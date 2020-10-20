from calm.dsl.builtins import Service, CalmVariable, CalmTask, action


class Arista(Service):
    # Variables for network provisioning
    CLUSTER_UUID = CalmVariable.Simple('', is_hidden=True, runtime=False)
    VLAN_ID = CalmVariable.Simple('', is_hidden=True, runtime=False)
    NETWORK_UUID = CalmVariable.Simple('', is_hidden=True, runtime=False)

    @action
    def __create__(self):
        CalmTask.SetVariable.escript(name='Get cluster UUID', filename='scripts/01-get_cluster_uuid.py',
                                     variables=['CLUSTER_UUID'])
        CalmTask.SetVariable.escript(name='Get vlan ID', filename='scripts/02-get_next_vlan_id.py',
                                     variables=['VLAN_ID'])
        CalmTask.Exec.escript(name='Check category', filename='scripts/03-check_category.py')
        CalmTask.Exec.escript(name='Check tenant key', filename='scripts/04-check_tenant_key.py')
        CalmTask.SetVariable.escript(name='Create new network', filename='scripts/05-create_new_network.py',
                                     variables=['NETWORK_UUID'])
        CalmTask.Exec.escript(name='Assign network to project', filename='scripts/06-update_project_network.py')
        CalmTask.Exec.escript(name='Create vlan on switch', filename='scripts/07-create_vlan_on_switch.py')
