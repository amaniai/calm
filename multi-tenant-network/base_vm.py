from calm.dsl.builtins import AhvVmResources, AhvVm
from calm.dsl.builtins import AhvVmDisk, AhvVmNic, AhvVmGC

from vars import VM_USERNAME, IMAGE_NAME, NETWORK_NAME


class CentOSVmResource(AhvVmResources):
    """Base CentOS VM Resource """

    memory = 4
    vCPUs = 2
    cores_per_vCPU = 1
    disks = [AhvVmDisk.Disk.Scsi.cloneFromImageService(IMAGE_NAME, bootable=True)]
    nics = [AhvVmNic.DirectNic.ingress(NETWORK_NAME)]
    guest_customization = AhvVmGC.CloudInit(
        config={
            'users': 
            [{
                'name': VM_USERNAME,
                'ssh-authorized-keys': ["@@{CENTOS_CRED.public_key}@@"],
                'sudo': ['ALL=(ALL) NOPASSWD:ALL']
            }]
        }
    )


class CentOSAhvVM(AhvVm):
    resources = CentOSVmResource
