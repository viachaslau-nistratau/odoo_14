from odoo import fields, models
from odoo.exceptions import ValidationError


class Partner(models.Model):
    """
    partner model классическое наследование - создание новой модели из существующей
    (res.partner), добавление новой информации к копии, но оставление исходной модели
    без изменения
    """
    _name = 'res.partner'
    _inherit = 'res.partner'

    published_book_ids = fields.One2many(
        'library.book',  # related model
        'publisher_id',  # field for 'this' on related model
        string='Published Books'
    )

    # book_id = fields.Many2one(
    #     'library.book',
    #     string='Authored Books',
    # )

    book_ids = fields.One2many(
        comodel_name='library.book',
        inverse_name='author_ids',
        string='Authored Books',
    )
