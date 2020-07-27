from calm.dsl.builtins import basic_cred, CalmTask, action
from calm.dsl.builtins import SimpleDeployment, SimpleBlueprint
from calm.dsl.builtins import read_provider_spec
from calm.dsl.builtins import CalmVariable
from calm.dsl.store import Secret

CENTOS = basic_cred('centos', 'nutanix/4u', name='CENTOS', default=True)
HYCU = basic_cred('admin', 'admin', name='HYCU', default=False)

class CentosDeployment(SimpleDeployment):
    provider_spec = read_provider_spec('specs/centos-8.yaml')
    os_type = 'Linux'

    @action
    def __create__(self):
        CalmTask.Exec.escript(name='add_vm_to_hycu', filename='scripts/add_vm_to_hycu.py')

    @action
    def __install__(self):
        # CalmTask.Exec.ssh(name='Update CentOS', script='sudo yum -y --quiet update')
        CalmTask.Exec.ssh(name='Update CentOS', script='echo "hello world"')


class HYCUCentOS8(SimpleBlueprint):
    credentials = [CENTOS, HYCU]
    deployments = [CentosDeployment]
    VM_NAME = CalmVariable.Simple.string('CentOS-VM', label='VM Name', runtime=True)
    
    # HYCU IP address, assuming default port for API access (8443)
    HYCU_IP = CalmVariable.Simple.string("10.38.4.21", runtime=False, is_hidden=True)

def main():
    print(HYCUCentOS8.json_dumps(pprint=True))

if __name__ == '__main__':
    main()