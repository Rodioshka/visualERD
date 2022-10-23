from core.config import DATABASE
# from .errors import (DropOrDeleteInRequestError, )

import psycopg2
from psycopg2 import Error, extras


class Database:
    def __init__(self):
        self._conn = psycopg2.connect(
            user=DATABASE['user'],
            password=DATABASE['password'],
            host=DATABASE['host'],
            port=DATABASE['port'],
            database=DATABASE['db']
        )

        self._cursor = self._conn.cursor(cursor_factory=extras.NamedTupleCursor)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()


if __name__ == '__main__':
    pass
