
from odoo import api, fields, models


class Book(models.Model):
    """
    model book
    """
    _inherit = "library.book"
    is_available = fields.Boolean('Is Available?')
    isbn = fields.Char(help="Use a valid ISBN-13 or ISBN-10.")
    publisher_id = fields.Many2one(index=True)

    # Логика предоставляемый базовым приложением библиотеки проверяет только
    # современные 13-значные номера ISBN, но некоторые более старые названия
    # могут иметь 10-значный ISBN. расширим метод _check_isbn () также на проверку этих случаев.

    def _check_isbn(self):
        self.ensure_one()
        digits = [int(x) for x in self.isbn if x.isdigit()]
        if len(digits) == 10:
            ponderators = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            total = sum(a * b for a, b in zip(digits[:9], ponderators))
            check = total % 11
            return digits[-1] == check
        else:
            return super()._check_isbn()

    # определяем его снова и в какой - то момент можем использовать super() для вызова
    # существующей реализации метода. В нашем методе мы проверяем, является ли это
    # 10-значным ISBN, и в этом случае выполняем недостающую логику проверки.
    # В противном случае мы вернемся к оригинальной логике проверки ISBN, которая
    # может обрабатывать 13-значный регистр.
