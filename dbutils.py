import os.path
import sqlite3

from pylib.paths import path

class DBConnection:

    def __init__(self, db):
        self.db = db
        self.conn = sqlite3.connect(str(path(db)))
        

class SqlCache():


    def __init__(self, sql_path):
        self.sql_path = sql_path
        self.sql_cache = {}


    def cache(self, label, sql_file=None, sql_statement=None):
        if not sql_cache.has_key(label):
            if sql_statement:
                self.sql_cache[lable] = sql_statement
            elif self.sql_path and sql_file:
                with path(os.path.join(self.sql_path, label)).open('r') as f:
                    self.sql_cache[label] = f.read()


    def statement(self, label):
        try:
            return self.sql_cache[label]
        except KeyError as e:
            self.cache(label, sql_file=label)
            return self.sql[label]


if __name__ == '__main__':
    pass
