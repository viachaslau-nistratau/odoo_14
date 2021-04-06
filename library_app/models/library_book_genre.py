from odoo import api, fields, models


class BookGenre(models.Model):
    """
    жанры книг
    """
    _name = 'library.book.genre'
    _description = 'Book Genre'
