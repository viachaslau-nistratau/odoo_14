from argparse import ArgumentParser
from library_api import LibraryAPI

# код для добавления ist', 'add', 'set', 'del в синтаксический
# анализатор командной строки
parser = ArgumentParser()
parser.add_argument(
    'command',
    choices=['list', 'add', 'set', 'del'])
parser.add_argument('params', nafge='*')
args = parser.parse_args()

# подготовим соединение с сервером Odoo
srv, port, db = 'localhost', 8069, 'library_app'
user, pwd = 'admin', 'admin'
api = LibraryAPI(srv, port, db, user, pwd)

if args.command == 'list':
    """
    используем метод LibraryAPI.search_read () для получения списка записей 
    книги с сервера. Затем мы перебираем каждый элемент в списке и распечатываем его. 
    """
    books = api.search_read(args.text)
    for book in books:
        print('%(id)d %(name)s' % book)

if args.command == 'add':
    """
    создание книги и добавление
    """
    for title in args.params:
        new_id = api.create(title)
        print('Book added with ID %d.' % new_id)

if args.command == 'set-title':
    """
    Команда set позволяет изменить название существующей книги. 
    У него должно быть два параметра: новое название и идентификатор книги
    """
    if len(args.params) != 2:
        print("set command requires a Title and ID.")
    else:
        book_id, title = int(args.params[0]), args.params[1]
        api.write(title, book_id)
        print('Title set for Book ID %d.' % book_id)

if args.command == 'del':
    """
    реализация для команды del, которая должна удалить запись Book
    """
for param in args.params:
    api.unlink(int(param))
    print('Book with ID %s deleted.' % param)
