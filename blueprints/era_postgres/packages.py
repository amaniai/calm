from calm.dsl.builtins import Package, ref

from services import Postgres


class PostgresPackage(Package):
    """Postgres Package on ERA"""
    services = [ref(Postgres)]

