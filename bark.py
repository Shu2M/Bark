import commands
import os


class Option:
    def __init__(self, name, command, prep_call=None):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def choose(self):
        data = self.prep_call() if self.prep_call else None
        message = self.command.execute(data) if data else self.command.execute()
        if isinstance(message, list):
            print('ID\tTITLE\tURL\tNOTE\tDATE')
            for m in message:
                print(*m, sep='\t')
        else:
            print(message)

    def __str__(self):
        return self.name


def print_options(options: dict) -> None:
    for shortcut, option in options.items():
        print(f'({shortcut}) {option}')


def option_choice_is_valid(choice: str, options: dict[str, Option]) -> bool:
    return choice in options or choice.upper() in options


def get_option_choice(options: dict[str: Option]) -> Option:
    choice = input('Выберете вариант дейсвия: ')
    while not option_choice_is_valid(choice, options):
        print('Недопустимый варинат')
        choice = input('Выберете вариант дейсвия: ')
    return options[choice.upper()]


def get_user_input(label, required=True) -> str:
    value = input(f'{label}: ') or None
    while required and not value:
        value = input(f'{label}: ') or None
    return value


def get_new_bookmark_data() -> dict:
    return {
        'title': get_user_input('Title'),
        'url': get_user_input('URL'),
        'notes': get_user_input('Notes', required=False)
    }


def get_bookmark_id_for_deletion() -> str:
    return get_user_input('Enter a bookmark ID to delete')


def clear_screen() -> None:
    clear = 'cls' if os.name == 'nt' else 'clear'
    os.system(clear)


def loop() -> None:
    clear_screen()
    print_options(options)
    user_option = get_option_choice(options)
    user_option.choose()
    input('Нажмите ENTER для возврата в меню...\n')


if __name__ == '__main__':
    commands.CreateBookmarksTableCommand().execute()
    options = {
        'A': Option(name='Добавить закладку', command=commands.AddBookmarkCommand(), prep_call=get_new_bookmark_data),
        'B': Option(name='Показать список закладок по дате', command=commands.ListBookmarksCommand()),
        'T': Option(name='Показать список закладок по заголовку', command=commands.ListBookmarksCommand(order_by='title')),
        'D': Option(name='Удалить закладку', command=commands.DeleteBookmarkCommand(), prep_call=get_bookmark_id_for_deletion),
        'Q': Option(name='Выйти', command=commands.QuitCommand())
    }
    while True:
        loop()
