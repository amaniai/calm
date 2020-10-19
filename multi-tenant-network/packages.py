from calm.dsl.builtins import Package, CalmTask, action, ref

from services import Arista


class AristaPackage(Package):
    """Arista Package"""
    services = [ref(Arista)]

