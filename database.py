import sqlite3
from typing import Union


class DatabaseManager:
    def __init__(self, database_filename: str) -> None:
        self.connection = sqlite3.connect(database_filename)

    def __del__(self):
        self.connection.close()

    def _execute(self, statement: str, values: Union[list, tuple] = None):
        with self.connection:  # создает контекст транзакции БД
            cursor = self.connection.cursor()
            cursor.execute(statement, values or None)
            return cursor

    def create_table(self, table_name: str, columns: dict) -> None:
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

    def add(self, table_nme: str, data: dict) -> None:
        placeholders = ', '.join('?' * len(data))
        column_names = ', '.join(data.keys())
        column_values = tuple(data.values())
        self._execute(
            f'''
            INSERT INTO {table_nme}
            ({column_names})
            VALUES ({placeholders});
            ''',
            column_values
        )

    def delete(self, table_name: str, criteria: dict) -> None:
        placeholders = [f'{column} = ?' for column in criteria.keys()]
        delete_criteria = ' AND '.join(placeholders)
        self._execute(
            f'''
            DELETE FROM {table_name}
            WHERE {delete_criteria};
            ''',
            tuple(criteria.values())
        )

    def select(self, table_name: str, criteria: dict = None, order_by=None):
        criteria = criteria or {}
        query = f'SELECT * FROM {table_name}'

        if criteria:
            placeholders = [f'{column} = ?' for column in criteria.keys()]
            select_criteria = ' AND '.join(placeholders)
            query += f' WHERE {select_criteria}'

        if order_by:
            query += f' ORDER BY {order_by}'

        self._execute(
            query,
            tuple(criteria.values())
        )
