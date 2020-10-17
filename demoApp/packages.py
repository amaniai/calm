from calm.dsl.builtins import Package, CalmTask, action, ref

from services import DemoApp, Haproxy, Postgres


class DemoAppPackage(Package):
    """DemoApp package"""
    services = [ref(DemoApp)]

    @action
    def __install__(self):
        CalmTask.Exec.ssh(name='update centos', filename='scripts/centos_update.sh')
        CalmTask.Exec.ssh(name='install docker', filename='scripts/centos_install_docker.sh')
        CalmTask.Exec.ssh(name='run demoApp', filename='scripts/run_demo-app_container.sh')


class HaproxyPackage(Package):
    """HAProxy package"""
    services = [ref(Haproxy)]

    @action
    def __install__(self):
        CalmTask.Exec.ssh(name='update centos', filename='scripts/centos_update.sh')
        CalmTask.Exec.ssh(name='install haproxy', filename='scripts/centos_install_haproxy.sh')


class PostgresPackage(Package):
    """Postgres Package on ERA"""
    services = [ref(Postgres)]

