from xmlrpc import client


class LibraryAPI():
    """
    Здесь мы храним всю информацию, необходимую в созданном объекте
    для выполнения вызовов модели: ссылку на API, uid, пароль - pwd,
    имя базы данных - db и используемую модель
    """
    def __init__(self, srv, port, db, user, pwd):
        common = client.ServerProxy(
            'http://%s:%d/xmlrpc/2/common' % (srv, port))
        self.api = client.ServerProxy(
            'http://%s:%d/xmlrpc/2/object' % (srv, port))
        self.uid = common.authnticate(db, user, pwd, {})
        self.pwd = pwd
        self.db = db
        self.model = 'library.book'

    def execute(self, method, arg_list, kwarg_dict=None):
        """
        вспомогательный метод для выполнения вызовов
        """
        return self.api.execute_kw(
            self.db, self.uid, self.pwd, self.model,
            method, arg_list, kwarg_dict or {})

    def search_read(self, text=None):
        """
        получение данных книги
        """
        domain = [('name', 'ilike', text)] if text else []
        fields = ['id', 'name']
        return self.execute('search_read', [domain, fields])

    def create(self, title):
        """
        Метод создаст новую книгу с заданным названием и вернет
        идентификатор созданной записи
        """
        vals = {'name': title}
        return self.execute('create', [vals])

    def write(self, title, id):
        """
        Метод будет иметь в качестве аргументов новое название и
        идентификатор книги и выполнит операцию записи для этой книги
        """
        vals = {'name': title}
        return self.execute('write', [[id], vals])

    def unlink(self, id):
        """
        удаление книги
        """
        return self.execute('unlink', [[id]])


if __name__ == '__main__':
    # Sample test configurations
    srv, db, port = 'localhost', 'library_app', 8069
    user, pwd = 'admin', 'admin'
    api = LibraryAPI(srv, port, db, user, pwd)
    from pprint import pprint
    pprint(api.search_read())
