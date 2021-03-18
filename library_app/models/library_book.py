from odoo import api, fields, models
from odoo.exceptions import Warning
# импорт объектов модулей и полей


class Book(models.Model): # новая модель
    _name = 'library.book'
    # атрибут _name, определяющий идентификатор,
    # который будет использоваться повсюду Odoo для обозначения этой модели
    _description = 'Book'
    # атрибут модели _description обеспечивает
    # удобное имя для записей модели, которое можно использовать для улучшения
    # пользовательских сообщений. Остальные строки определяют поля модели.
    name = fields.Char('Title', required=True)
    isbn = fields.Char('ISBN')
    active = fields.Boolean('Active?', default=True)
    date_published = fields.Date()
    image = fields.Binary('Cover')
    publisher_id = fields.Many2one('res.partner', string='Publisher')
    author_ids = fields.Many2many('res.partner', string='Authors')

    @api.multi
    def _check_isbn(self): #проверка ISBN
        self.ensure_one()
        digits = [int(x) for x in self.isbn if x.isdigit()]
        if len(digits) == 13:
            ponderations = [1, 3] * 6
            terms = [a * b for a, b in zip(digits[:12], ponderations)]
            remain = sum(terms) % 10
            check = 10 - remain if remain != 0 else 0
        return digits[-1] == check

    @api.multi
    def button_check_isbn(self): # использование предыдущей функции для проверки ISBN
        for book in self:
            if not book.isbn:
                raise Warning('Please provide an ISBN for %s' % book.name)
            if book.isbn and not book._check_isbn():
                raise Warning('%s is an invalid ISBN' % book.isbn)
        return True