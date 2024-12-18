import os
import sqlite3
import sys


class SQLightDatabase:
    def __init__(self, database_name, dict_cursor=False):
        self.database_name = database_name
        self.connection = None
        self.dict_cursor = dict_cursor

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self, autocommit=True, check_same_thread=True, foreign_keys=True):
        self.connection = sqlite3.connect(
            self.database_name, autocommit=autocommit, check_same_thread=check_same_thread
        )
        if self.dict_cursor:
            self.connection.row_factory = dict_factory
        if foreign_keys:
            self.execute("PRAGMA foreign_keys = ON;")
        return self.connection

    def close(self, optimize=True):
        if optimize:
            self.execute("PRAGMA optimize;")
        self.connection.close()

    def execute(self, query, parameters=()):
        cursor = self.connection.cursor()
        cursor.execute(query, parameters)

        return cursor

    def fetch_one(self, query, parameters=()):
        return self.execute(query, parameters).fetchone()

    def fetch_all(self, query, parameters=()):
        return self.execute(query, parameters).fetchall()

    def toggle_dict_cursor(self, state: bool):
        self.dict_cursor = state
        self.connection.row_factory = dict_factory if state else None


def database_connect(dict_cursor=False) -> SQLightDatabase:
    return SQLightDatabase(os.environ["AGGREGATOR_DB_NAME"], dict_cursor)


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}


def database_reader_connection(dict_cursor=False):
    if not hasattr(database_reader_connection, "connection"):
        database_reader_connection.connection = SQLightDatabase(os.environ["AGGREGATOR_DB_NAME"], dict_cursor)
        database_reader_connection.connection.connect(check_same_thread=False)
    database_reader_connection.connection.toggle_dict_cursor(dict_cursor)
    return database_reader_connection.connection


def check_and_set_threadsafety():
    if sqlite3.threadsafety == 0:
        sys.exit("Бібліотека sqlite3 зібрана в режимі однопоточності.")
    sqlite3.threadsafety = 3
