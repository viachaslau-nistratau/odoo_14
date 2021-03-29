from odoo import fields, models


class CheckoutStage(models.Model):
    """
    модуль стадии запроса книг
    """
    _name = 'library.checkout.stage'
    _description = 'Checkout Stage'
    _order = 'sequence,name'

    # name = fields.Char(translation=True)
    name = fields.Char()
    sequence = fields.Integer(default=10)
    fold = fields.Boolean()
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [('new', 'New'),
         ('open', 'Borrowed'),
         ('done', 'Returned'),
         ('cancel', 'Cancelled')],
        default='new',
    )

    #  state - поле состояния, позволяющее сопоставить каждый этап с одним из четырех
    #  разрешенных основных состояний.
    # Поле sequence важно. Чтобы настроить порядок, этапы должны быть представлены на доске
    # Канбан и в списке выбора этапов.
    # Логическое поле fold будет использоваться канбан-доской для некоторых столбцов,
    # свернутых по умолчанию, так что их содержимое не сразу становится доступным.
    # Обычно это используется для этапов «Выполнено» и «Отменено» (done and Cancelled).
