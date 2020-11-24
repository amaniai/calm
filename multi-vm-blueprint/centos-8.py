from calm.dsl.builtins import basic_cred, CalmTask, action
from calm.dsl.builtins import SimpleDeployment, SimpleBlueprint
from calm.dsl.builtins import read_provider_spec
from calm.dsl.builtins import CalmVariable
from calm.dsl.store import Secret

CENTOS = basic_cred('nutanix', 'nutanix/4u', name='CENTOS', default=True)

class CentosDeployment(SimpleDeployment):
    provider_spec = read_provider_spec('specs/centos-8.yaml')
    os_type = 'Linux'

    @action
    def __create__(self):
        # CalmTask.Exec.escript(name='add_vm_to_hycu', filename='scripts/add_vm_to_hycu.py')

    @action
    def __install__(self):
        # CalmTask.Exec.ssh(name='Update CentOS', script='sudo yum -y --quiet update')
        # CalmTask.Exec.ssh(name='Update CentOS', script='echo "hello world"')


class MultiVMBlueprint(SimpleBlueprint):
    credentials = [CENTOS]
    deployments = [CentosDeployment]
    VM_NAME = CalmVariable.Simple.string('CentOS-VM', label='VM Name', runtime=True)
    


def main():
    print(MultiVMBlueprint.json_dumps(pprint=True))

if __name__ == '__main__':
    main()