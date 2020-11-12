from calm.dsl.builtins import Package, ref

from services import Oracle


class OraclePackage(Package):
    """Postgres Package on ERA"""
    services = [ref(Oracle)]

