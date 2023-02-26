from database import DatabaseManager
from datetime import datetime
import sys


db = DatabaseManager(database_filename='bookmarks.db')


class CreateBookmarksTableCommand:
    @staticmethod
    def execute() -> None:
        db.create_table(table_name='bookmarks', columns={
            'id': 'integer primary key autoincrement',
            'title': 'text not null',
            'url': 'text not null',
            'notes': 'text',
            'date_added': 'text not null'
        })


class AddBookmarkCommand:
    @staticmethod
    def execute(data: dict) -> str:
        data['date_added'] = datetime.utcnow().isoformat()
        db.add('bookmarks', data)
        return 'Закладка добавлена'


class ListBookmarksCommand:
    def __init__(self, order_by: str = 'date_added') -> None:
        self.order_by = order_by

    def execute(self):
        return db.select('bookmarks', order_by=self.order_by).fetchall()


class DeleteBookmarkCommand:
    @staticmethod
    def execute(data) -> str:
        db.delete('bookmarks', criteria={'id': data})
        return 'Закладка удалена'


class QuitCommand:
    @staticmethod
    def execute() -> None:
        sys.exit()
