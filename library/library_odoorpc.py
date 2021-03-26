from odoorpc import ODOO


class LibraryAPI():
    """
    Здесь мы храним всю информацию, необходимую в созданном объекте
    для выполнения вызовов модели: ссылку на API, uid, пароль - pwd,
    имя базы данных - db и используемую модель
    альтернативная реализация интерфейса library_api.py с сервером
    """
    def __init__(self, srv, port, db, user, pwd):
        self.api = ODOO(srv, port=port)
        self.api.login(db, user, pwd)
        self.uid = self.api.env.uid
        self.model = 'library.book'
        self.Model = self.api.env[self.model]

    def execute(self, method, arg_list, kwarg_dict=None):
        """
        вспомогательный метод для выполнения вызовов
        """
        return self.api.execute(
            self.model,
            method, *arg_list, **kwarg_dict)

    def search_read(self, text=None):
        domain = [('name', 'ilike', text)] if text else []
        fields = ['id', 'name']
        return self.Model.search_read(domain or [], fields)

    def create(self, title):
        vals = {'name': title}
        return self.Model.create(vals)

    def write(self, title, id):
        vals = {'name': title}
        self.Model.write(id, vals)

    def unlink(self, id):
        return self.Model.unlink(id)


if __name__ == '__main__':
    srv, port, db = 'localhost', 8069, 'library_app'
    user, pwd = 'admin', 'admin'
    api = LibraryAPI(srv, port, db, user, pwd)
    from pprint import pprint
    pprint(api.search_read())
