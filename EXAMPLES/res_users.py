from odoo import models, fields, api
from odoo.exceptions import ValidationError

    # НАСЛЕДОВАНИЕ В ODOO

class Users(models.Model):
    '''
    расширение существующей модели (res.users),
    добавление нового функционала (новых полей или методов),
    новая модель данных заменит собой уже существующую
    '''
    _name = 'res.users'
    _inherit = 'res.users'

class ForeignPartners(models.Model):
    """
    создание новой модели данных из существующей модели
    (к примеру domestic.partners),
    добавление нового функционала (новых полей или методов),
    но оставление исходной модели без изменения
    """
    _name = 'foreign.partners'
    _inherit = 'domestic.partners'

    # СВЯЗАННЫЕ ПОЛЯ (RELATED FIELDS)
    # по умолчанию значения связанных полей не сохраняются в БД.
    # добавление параметра store = True позволяет сохранить значение

    # использование связанного (related) поля
    # в модели library.book имелось реляционное поле member_book_id,
    # которое было связано с моделью library.member отношением many2one
    # с реляционным полем partner_id,
    # которое в свою очередь было связано с моделью res.partner отношением many2one.
    # а уже из модели res.partner получили значение поля display_name

    member_card_number = fields.Char(
        related='member_book_id.partner_id.display_name',
        store=True,
    )

    # ВЫЧИСЛЯЕМЫЕ ПОЛЯ (COMPUTE FIELDS)

    # вычисляемые поля по умолчанию не сохраняются,
    # их значения вычисляются и возвращаются по запросу,
    # параметр store = True сохранит их значение в базе данных
    # использование декоратора @api.depends,
    # название метода начинается с _compute

    name = fields.Char(
        string='Название книги',
        size=35,
    )
    date_published = fields.Date(
        'Год издания',
    )
    author_id = fields.Many2one(
        comodel_name='res.partner',
        string='Автор',
    )

    # создание вычисляемого поля add_info
    add_info = fields.Char(
        string='Автор/Название книги/Год издания',
        compute='_compute_name_author',
        readonly=True,
    )

    add_info = fields.Char(
        string='Автор/Название книги/Год издания',
        compute='_compute_name_author',
        inverse='_set_name_author',
    )

    @api.depends('name', 'author_id.name', 'date_published')
    def _compute_name_author(self):
        """
        функция конкатенации 3-х полей - автора, названия книги
        и даты публикации
        использование метода strftime("%Y") - удаление месяца и дня
        """
        for book in self:
            name_book = book.name
            author = book.author_ids.name
            if book.date_published:
                year = book.date_published.strftime("%Y")
            else:
                year = 'Год издания не известен'
            book.add_info = f'{author} - {name_book} ({year})'

    def _set_name_author(self):
        """
        метод позволяющий сделать поле add_info редактируемым
        """
        for book in self:
            if not book.add_info:
                continue
            with open(book._compute_name_author) as f:
                f.write(book.add_info)

    # создание вычисляемого поля date_published, только год издания
    date_published = fields.Date(
        compute='_compute_change_date',
    )

    @api.depends('date_published')
    def _compute_change_date(self):
        """
        метод переводящий формат даты ДД.ММ.ГГ просто в год
        """
        for book in self:
            if book.date_published:
                book.date_published = book.date_published.strftime("%Y")

    # ИСПОЛЬЗОВАНИЕ ДЕКОРАТОРОВ @api.constrains, @api.model,
    # @api.onchange (название метода начинается с onchange)

    # создание случайного поля
    name = fields.Char(
        string='абракадабра',
    )

    @api.constrains('name')
    def change_name(self):
        """
        использование декоратора - constrains для проверки на наличие
        дубликата записи в поле - name, создание метода change_name
        """
        for record in self:
            is_duble_name = self.env['res.users'].search_count([
                ('name', '=', record.name),
                ('id', '!=', record.id),
            ])
            if is_duble_name:
                raise ValidationError('Такое имя уже есть')

    @staticmethod
    def name_without_space(vals):
        """
        создание метода name_without_space, проверка наличия ключа 'name' в vals,
        получение по ключу с помощью метода get() соответствующего значения,
        в случае наличия значения, с помощью метода strip() удаление пробелов
        справа и слева
        """
        if 'name' in vals:
            name_value = vals.get('name', '')
            if name_value:
                vals['name'] = name_value.strip()

    @api.model
    def create(self, vals):
        """
        модуль запуска метода  name_without_space при создании новой записи
        переход на другое поле (ввод или по стрелке)
        """
        self.name_without_space(vals)
        res = super().create(vals)
        return res

    def write(self, vals):
        """
        модуль запуска метода  name_without_space при сохранении новой записи
        переход на другое поле (ввод или по стрелке)
        """
        self.name_without_space(vals)
        res = super().write(vals)
        return res

    @api.onchange('tr_carrier_drv_last_name')
    def onchange_last_name_driver(self):
        """
        использование декоратора onchange
        создание метода onchange_last_name_driver для перевода в верхний регистр
        фамилии водителя
        """
        for record in self:
            if record.tr_carrier_drv_last_name:
                upper_record_driver_name = record.tr_carrier_drv_last_name.upper()
                record.tr_carrier_drv_last_name = upper_record_driver_name

    def upper_register(self):
        """
        функция перевода в верхний регистр названия книги
        """
        for book in self:
            str(book.name).upper() if book.name else False

    @api.onchange('check_button')
    def _all_checked(self):
        """
        функция реализации чекбокса (вызов скрытого поля)
        """
        if self.check_button:
            self.check_button = False
        else:
            self.check_button = True

    def date_take_book_in_library(self):
        """
        дата получения книги пользователем
        """
        self.write({
            'date_take_book': fields.Date.today(),
        })
        return True

    def _compute_date_return_book(self):
        """
        дата, когда необходимо вернуть книгу в библиотеку
        """
        for member in self:
            if member.date_take_book:
                self.write({
                    'date_return': fields.Date.today() + timedelta(days=10),
                })
                return True
            else:
                pass