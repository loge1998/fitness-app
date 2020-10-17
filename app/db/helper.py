from contextlib import contextmanager
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import ThreadedConnectionPool
from app.core.config import config
import logging


class DbConnectionPool:

    __pool = None

    @staticmethod
    def get_db_connection_pool():
        if not DbConnectionPool.__pool:
            logging.info("DbConnectionPool initialising connection pool")
            DbConnectionPool.__pool = ThreadedConnectionPool(1, 10,
                                                             database=config.DB_NAME,
                                                             user=config.DB_USERNAME,
                                                             password=config.DB_PASSWORD,
                                                             host=config.DB_HOST,
                                                             port=config.DB_PORT
                                                             )
        return DbConnectionPool.__pool

    @staticmethod
    def close():
        if DbConnectionPool.__pool:
            logging.info("DbConnectionPool closing connection pool")
            DbConnectionPool.__pool.closeall()
            DbConnectionPool.__pool = None


@contextmanager
def get_db_connection():
    connection = None
    try:
        connection = DbConnectionPool.get_db_connection_pool().getconn()
        yield connection
    finally:
        DbConnectionPool.get_db_connection_pool().putconn(connection)


@contextmanager
def get_db_cursor(commit=False):
    with get_db_connection() as connection:
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            yield cursor
            if commit:
                connection.commit()
        finally:
            cursor.close()
