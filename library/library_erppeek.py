from erppeek import Client


class LibraryAPI():
    """
    Здесь мы храним всю информацию, необходимую в созданном объекте
    для выполнения вызовов модели: ссылку на API, uid, пароль - pwd,
    имя базы данных - db и используемую модель
    альтернативная реализация интерфейса library_api.py с сервером
    """
    def __init__(self, srv, port, db, user, pwd):
        self.Client = Client(
            'http://%s:%d' % (srv, port), db, user, pwd)
        self.model = 'library.book'

    def execute(self, method, arg_list, kwarg_dict=None):
        """
        вспомогательный метод для выполнения вызовов
        """
        return self.Client.execute(
            self.model,
            method, *arg_list, **kwarg_dict)

    def search_read(self, text=None):
        domain = [('name', 'ilike', text)] if text else []
        fields = ['id', 'name']
        return self.Client.read(self.model, domain, fields)

    def create(self, title):
        vals = {'name': title}
        return self.Client.create(self.model, vals)

    def write(self, title, id):
        vals = {'name': title}
        self.Client.write(self.model, [id], vals)

    def unlink(self, id):
        return self.Client.unlink(self.model, id)


if __name__ == '__main__':
    srv, port, db = 'localhost', 8069, 'library_app'
    user, pwd = 'admin', 'admin'
    api = LibraryAPI(srv, port, db, user, pwd)
    from pprint import pprint
    pprint(api.search_read())
