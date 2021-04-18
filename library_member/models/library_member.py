from datetime import timedelta

from odoo import fields, models, api


class Member(models.Model):
    """
    пользователи библиотеки
    """
    _name = 'library.member'
    _description = 'Library Member'
    # _order = 'card_number'
    # наследование от классов миксинов выполняется с помощью _inherit атрибута.
    # надо сделать так, чтобы класс унаследовал mail.thread
    # и mail.activity.mixin миксин классов
    _inherit = ['mail.thread', 'mail.activity.mixin']

    user_image = fields.Binary(string='Фотография пользователя библиотеки')

    # фамилия, имя, отчество
    name = fields.Char(
        string='ФИО',
        size=40, )
    # requered = True,

    card_number = fields.Char(string='Номер абонемента пользователя',
                              compute='number_card_member',
                              size=2)
    # number_member = fields.Char(string='Номер абонемента пользователя',)
    #
    # check_button_number = fields.Boolean(string='Примечание')

    # Дата регистрации в библиотеке, дата ухода
    date_start_library = fields.Date(
        string='Дата регистрации в библиотеке')
    date_finish_library = fields.Date(
        string='Дата окончания пользования библиотекой')

    count_book = fields.Integer(string='Количество книг на руках')

    # Блок персональной информации
    personal_info = fields.Boolean(string='Персональная информация')
    home_address_member = fields.Char(string='Домашний адрес', size=100)
    mobil_phone = fields.Char(string='Номер мобильного телефона', size=15)
    home_phone = fields.Char(string='Номер домашнего телефона', size=15)

    # Блок информации о месте работы
    info_about_place_job = fields.Boolean(string='Информация о месте работы')
    job_member = fields.Char(string='Место работы')
    job_phone = fields.Char(string='Рабочий телефон')

    # Блок информации о взятых в библиотеке книгах
    info_about_borrowed_book = fields.Boolean(
        string='Информация о взятых в пользование книгах')
    name_book = fields.Char(string='Книги',
                            translate=True, required=True)
    member_book_ids = fields.One2many('library.book', 'member_book_id', string='')

    # info_about_book = fields.Char(string='Информация о взятых в пользование книгах')
    # name = fields.One2many(comodel_name='library.book',
    #                        string='Название книги', )
    date_take_book = fields.Date(string='Дата получения книги',)
    date_return = fields.Date(string='Дата возврата книги',)
                              # compute='date_return_book',
                              # )
    alarm_date = fields.Char(string='Примечание',
                             compute='_alarm_date_return',
                             readonly=False,
                             )

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

    @api.depends()
    def number_card_member(self):
        """
        присвоение порядкового номера при регистрации
        нового пользователя
        """
        for member in self:
            member.card_number = str(member.id)
            # member_qty = self.search_count([])
            # print('member_qty = ', member_qty)

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

    # def date_take_book_in_library(self):
    #     """
    #     дата получения книги пользователем
    #     """
    #     self.write({
    #         'date_take_book': fields.Date.today(),
    #     })
    #     return True

    # def date_return_book(self):
    #     """
    #     дата, когда необходимо вернуть книгу в библиотеку
    #     """
    #     self.write({
    #         'date_return': 'date_take_book' + timedelta(days=1),
    #     })
    #     return True

    # 'date_return': fields.Date.today() + timedelta(days=1),


    def _alarm_date_return(self):
        """
        проверка истечения срока пользования книгой
        """
        for member in self:
            date_now = fields.Date.today()
            if member.date_return == date_now:
                note = 'ВНИМАНИЕ!!! Срок пользования книгой закончился'
            else:
                note = 'Срок пользования книгой не закончился'
            member.alarm_date = f'{note}'

    # def _compute_date_return_book(self):
    #     """
    #     дата, когда необходимо вернуть книгу в библиотеку
    #     """
    #     for member in self:
    #         if member.date_take_book:
    #             self.write({
    #                 'date_return': fields.Date.today() + timedelta(days=1),
    #             })
    #             return True
    #         else:
    #             pass
