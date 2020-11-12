from calm.dsl.builtins import Package, ref

from services import Mssql


class MssqlPackage(Package):
    """Postgres Package on ERA"""
    services = [ref(Mssql)]

