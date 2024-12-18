import sqlite3

from utils.database import database_connect
from utils.logger import logger


def database_writer(database_edit_queue, database_response_queue):
    """One process responsible for all database write operations"""
    conn = database_connect().connect()
    c = conn.cursor()

    # Сигналізуємо основному процесу що можна починати редагувати базу
    database_response_queue.put(True)

    try:
        while True:
            try:
                # items should be list of lists
                command, items = database_edit_queue.get()
                c.executemany(command, items)
            except sqlite3.Error as ex:
                conn.rollback()
                logger.error(f"Помилка запису до бази: {str(ex)}")
    except KeyboardInterrupt:
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        conn.close()
        database_edit_queue.close()
        database_response_queue.close()
