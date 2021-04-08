from odoo import fields, models


class Member(models.Model):
    """
    пользователи библиотеки
    """
    _name = 'library.member'
    _description = 'Library Member'
    # наследование от классов миксинов выполняется с помощью _inherit атрибута.
    # надо сделать так, чтобы класс унаследовал mail.thread
    # и mail.activity.mixin миксин классов
    _inherit = ['mail.thread', 'mail.activity.mixin']

    image = fields.Binary(string='Фотография')

    # фамилия, имя, отчество
    family_name_surname = fields.Char(
        string='ФИО',
        requered=True,
        size=40,)

    # учетный номер
    card_number = fields.Char(string='Учетный номер', size=4)

    # Дата регистрации в библиотеке, дата ухода
    date_start_library = fields.Date(string='Дата регистрации в библиотеке')
    date_finish_library = fields.Date(string='Дата окончания')

    partner_id = fields.Many2one(
        'res.partner',
        delegate=True,
        ondelete='cascade',
        required=True
    )

    # При наследовании с делегированием модель library.member встраивает
    # унаследованные Модель, res.partner, так что при создании новой
    # записи Участника связанный Партнер автоматически создается и указывается
    # в поле partner_id.
