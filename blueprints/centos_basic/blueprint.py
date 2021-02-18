# THIS FILE IS AUTOMATICALLY GENERATED.
# Disclaimer: Please test this file before using in production.
"""
Generated blueprint DSL (.py)
"""

import json  # no_qa
import os  # no_qa

from calm.dsl.builtins import *  # no_qa


# Secret Variables
BP_CRED_CENTOS_PASSWORD = read_local_file("BP_CRED_CENTOS_PASSWORD")

# Credentials
BP_CRED_CENTOS = basic_cred(
    "centos",
    BP_CRED_CENTOS_PASSWORD,
    name="CENTOS",
    type="PASSWORD",
    default=True,
)


centos_8_3_cloud = vm_disk_package(
    name="centos_8_3_cloud",
    description="Standard CentOS 8.3 cloud image",
    config={
        "name": "centos_8_3_cloud",
        "image": {
            "name": "centos_8_3_cloud",
            "type": "DISK_IMAGE",
            "source": "https://cloud.centos.org/centos/8/x86_64/images/CentOS-8-GenericCloud-8.3.2011-20201204.2.x86_64.qcow2",
            "architecture": "X86_64",
        },
        "product": {"name": "CentOS", "version": "8.3"},
        "checksum": {},
    },
)


class CentOS(Service):

    pass


class VMResources(AhvVmResources):

    memory = 1
    vCPUs = 1
    cores_per_vCPU = 1
    disks = [
        AhvVmDisk.Disk.Scsi.cloneFromVMDiskPackage(centos_8_3_cloud, bootable=True)
    ]
    nics = [
        AhvVmNic.NormalNic.ingress("Network-02", cluster="Middle-East-Lab-cluster2")
    ]

    guest_customization = AhvVmGC.CloudInit(
        filename=os.path.join("specs", "VM_cloud_init_data.yaml")
    )


class CentosAHV(AhvVm):

    name = "centos-@@{calm_random}@@"
    resources = VMResources


class CentosVM(Substrate):

    os_type = "Linux"
    provider_type = "AHV_VM"
    provider_spec = CentosAHV
    provider_spec_editables = read_spec(
        os.path.join("specs", "VM_create_spec_editables.yaml")
    )
    readiness_probe = readiness_probe(
        connection_type="SSH",
        disabled=False,
        retries="5",
        connection_port=22,
        address="@@{platform.status.resources.nic_list[0].ip_endpoint_list[0].ip}@@",
        delay_secs="20",
    )


class PackageUbuntu(Package):

    services = [ref(CentOS)]

    @action
    def __install__(self):

        CalmTask.Exec.escript(
            name="resize_disk",
            filename=os.path.join(
                "scripts",
                "action___install___Task_resize_disk.py",
            ),
            target=ref(CentOS),
        )
        CalmTask.Exec.ssh(
            name="update_os",
            filename=os.path.join(
                "scripts", "action___install___Task_update_os.sh"
            ),
            target=ref(CentOS),
        )
        CalmTask.Delay(
            name="wait_for_disk_resize", delay_seconds=20, target=ref(CentOS)
        )
        CalmTask.Delay(name="wait_for_reboot", delay_seconds=20, target=ref(CentOS))


class DefaultDeployment(Deployment):

    min_replicas = "1"
    max_replicas = "1"
    default_replicas = "1"

    packages = [ref(PackageUbuntu)]
    substrate = ref(CentosVM)


class Default(Profile):

    deployments = [DefaultDeployment]


class CentOSBasic(Blueprint):
    """CentOS server 8.3 basic installation """

    services = [CentOS]
    packages = [PackageUbuntu, centos_8_3_cloud]
    substrates = [CentosVM]
    profiles = [Default]
    credentials = [BP_CRED_CENTOS]