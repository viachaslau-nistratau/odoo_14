from odoo import api, fields, models


class Checkout(models.Model):
    """
    модуль выбора книг
    """
    _name = 'library.checkout'
    _description = 'Checkout Request'
    member_id = fields.Many2one(
        'library.member',
        required=True)
    user_id = fields.Many2one(
        'res.users',
        string='Librarian',
        default=lambda s: s.env.uid)
    request_date = fields.Date(
        default=lambda s: fields.Date.today())
    line_ids = fields.One2many(
        'library.checkout.line',
        'checkout_id',
        string='Borrowed Books', )


class CheckoutLine(models.Model):
    """
    модуль проверки выбора книг
    """
    _name = 'library.checkout.line'
    _description = 'Borrow Request Line'
    checkout_id = fields.Many2one('library.checkout')
    book_id = fields.Many2one('library.book')
