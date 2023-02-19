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

    def crete_table(self, table_name: str, columns: dict) -> None:
        columns_with_types = [
            f"{column_name} {column_type}"
            for column_name, column_type in columns.items()
        ]
        self._execute(
            f'''
            CREATE TABLE IF NOT EXIST {table_name}
            ({', '.join(columns_with_types)});
            '''
        )
