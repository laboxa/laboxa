from contextlib import contextmanager
import pymysql
from pymysql.cursors import DictCursor
from config import DatabaseConfig

class DatabaseManager:
    def __init__(self, config: DatabaseConfig):
        self.config = config

    @contextmanager
    def get_connection(self):
        connection = None
        try:
            connection = pymysql.connect(
                host=self.config.host,
                user=self.config.user,
                password=self.config.password,
                database=self.config.database,
                charset=self.config.charset,
                cursorclass=DictCursor
            )
            yield connection
        except Exception as e:
            if connection:
                connection.rollback()
            raise e
        finally:
            if connection:
                connection.close()

    @contextmanager
    def get_cursor(self):
        with self.get_connection() as connection:
            cursor = connection.cursor()
            try:
                yield cursor
                connection.commit()
            except Exception as e:
                connection.rollback()
                raise e
            finally:
                cursor.close()