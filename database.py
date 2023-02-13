import sqlite3


class DatabaseManager:
    def __init__(self, database_filename: str) -> None:
        self.connection = sqlite3.connect(database_filename)

    def __del__(self):
        self.connection.close()

    def _execute(self, statement: str, values: list = None):
        with self.connection:  # создает контекст транзакции БД
            cursor = self.connection.cursor()
            cursor.execute(statement, values or None)
            return cursor

