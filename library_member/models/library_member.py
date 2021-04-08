from odoo import fields, models


class Member(models.Model):
    """
    пользователи библиотеки
    """
    _name = 'library.member'
    _description = 'Library Member'
    _order = 'family_name_surname'
    # наследование от классов миксинов выполняется с помощью _inherit атрибута.
    # надо сделать так, чтобы класс унаследовал mail.thread
    # и mail.activity.mixin миксин классов
    _inherit = ['mail.thread', 'mail.activity.mixin']

    user_image = fields.Binary(string='Фотография пользователя библиотеки')

    # фамилия, имя, отчество
    family_name_surname = fields.Char(
        string='ФИО',
        requered=True,
        size=40,)

    # учетный номер
    card_number = fields.Char(string='Номер абонемента', size=4)

    # Дата регистрации в библиотеке, дата ухода
    date_start_library = fields.Date(string='Дата регистрации в библиотеке')
    date_finish_library = fields.Date(
        string='Дата окончания пользования библиотекой')

    # Блок персональной информации
    check_button_info = fields.Boolean(string='Персональная информация')
    # personal_info = fields.Boolean(string='Персональная информация')
    home_address_member = fields.Char(string='Домашний адрес', size=100)
    mobil_phone = fields.Char(string='Номер мобильного телефона', size=15)
    home_phone = fields.Char(string='Номер домашнего телефона',size=15)

    # Блок информации о месте работы
    check_button_job = fields.Boolean(string='Информация о месте работы')
    # info_about_job = fields.Char(string='Информация о месте работы')
    job_member = fields.Char(string='Место работы')
    job_phone = fields.Char(string='Рабочий телефон')

    # Блок информации о взятых в библиотеке книгах
    check_button_book = fields.Boolean(string='Информация о взятых в пользование книгах')
    # info_about_book = fields.Char(string='Информация о взятых в пользование книгах')
    # name = fields.One2many(comodel_name='library.book',
    #                        string='Название книги', )
    date_take_book = fields.Date(string='дата получения книги')
    date_return = fields.Date(string='Дата возврата книги')

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

    def date_reg_in_library(self):
        """
        кнопка регистрации пользователя (абонента) в библиотеке
        """
        self.write({
            'date_start_library': fields.Date.today(),
        })
        return True

    def date_out_library(self):
        """
        кнопка завершения периода пользования библиотекой
        """
        self.write({
            'date_finish_library': fields.Date.today(),
        })
        return True
