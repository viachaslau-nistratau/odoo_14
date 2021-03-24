# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import Warning
from odoo.exceptions import ValidationError

# импорт объектов модулей и полей


class Book(models.Model):
    """
    model book
    """
    _name = 'library.book'
    # атрибут _name, определяющий идентификатор,
    # который будет использоваться повсюду Odoo для обозначения этой модели
    _description = 'Book'
    # атрибут модели _description обеспечивает
    # удобное имя для записей модели, которое можно использовать для улучшения
    # пользовательских сообщений. Остальные строки определяют поля модели.
    # в нашем случае - упорядочен по умолчанию по названию книги,
    # а затем в обратном порядке дата публикации (от самой новой до самой старой)
    _order = 'name, date_published desc'
    # _order устанавливает порядок по умолчанию для использования
    # при просмотре записей модели, или отображается в виде списка.

    # Text fields
    # использование аргументов ключевого слова для атрибутов поля:
    name = fields.Char(
        'Title',
        default=None,
        index=True,
        help='Book cover title',
        readonly=False,
        required=True,
        translate=False,
    )

    # String fields: name = fields.Char('Title')
    # Char (string) - это одна строка текста.
    # Единственный ожидаемый позиционный аргумент: метка строкового поля
    isbn = fields.Char('ISBN')
    # Selection (selection, string) - это раскрывающийся список выбора.
    # Выбор позиционных аргументов - это список кортежей [('value', 'Title'),].
    # Первый элемент кортежа - это значение, хранящееся в базе данных.
    # Второй элемент кортежа - это описание представленое в пользовательском интерфейсе.
    # Этот список может быть расширен другими модулями, используя аргумент ключевого
    # слова selection_add.
    book_type = fields.Selection(
        [('paper', 'Paperback'),
         ('hard', 'Hardcover'),
         ('electronic', 'Electronic'),
         ('other', 'Other')],
        'Type')
    # Text многострочный текст. Единственный позиционный аргумент - это строка, метка поля
    notes = fields.Text('Internal Notes')
    # Html хранится как текстовое поле, но имеет специфическую обработку пользователя
    # интерфейса для представления содержимого HTML
    descr = fields.Html('Description')

    # Numeric fields
    # Integer (string) просто ожидает строковый аргумент для заголовка поля.
    copies = fields.Integer(default=1)
    # Float (string, digits) имеет второй необязательный аргумент - цифры, как (x, y)
    # кортеж с точностью поля. x - общее количество цифр; из них y десятичные цифры.
    avg_rating = fields.Float('Average Rating', (3, 2))
    # Monetary (string, currency_field) похоже на поле с плавающей запятой,
    # но имеет особую обработку валюты. Используется второй аргумент currency_field
    # для установки поля, в котором хранится используемая валюта.
    # По умолчанию ожидается поле currency_id.
    price = fields.Monetary('Price', 'currency_id')

    currency_id = fields.Many2one('res.currency')

    # Date and time fields
    # Date (string) и Datetime(string) ожидают только текст строки как позиционный аргумент.
    date_published = fields.Date()
    # вычисление значения по умолчанию с текущими датой и временем:
    last_borrow_date = fields.Datetime(
        'Last Borrowed One',
        default=lambda self: fields.Datetime.now()
    )

    # Other fields
    # Boolean(string) содержит значения True или False, как и следовало ожидать,
    # и имеет только один позиционный аргумент для текстовой строки.
    active = fields.Boolean('Active?', default=True)
    # Binary(string) хранит двоичные данные в виде файлов, а также ожидает только строку аргумент.
    # может быть обработано кодом Python с использованием строк в кодировке base64.
    image = fields.Binary('Cover')

    # Relation fields
    # поле publisher_id представляет издателя книги и является
    # ссылкой на запись в партнерской модели
    publisher_id = fields.Many2one('res.partner', string='Publisher')
    # связь "многие ко многим" между книгами и авторами: у каждой книги
    # может быть много авторов, и у каждого автора может быть много книг
    author_ids = fields.Many2many('res.partner', string='Authors')

    def button_check_isbn(self):
        """
        использование  функции _check_isbn для проверки isbn
        """
        for book in self:
            if not book.isbn:
                raise Warning('Please provide an ISBN for %s' % book.name)
            if book.isbn and not book._check_isbn():
                raise Warning('%s is an invalid ISBN' % book.isbn)
        return True

    def _check_isbn(self):
        """
        проверка isbn
        """
        self.ensure_one()
        digits = [int(x) for x in self.isbn if x.isdigit()]
        if len(digits) == 13:
            ponderations = [1, 3] * 6
            terms = [a * b for a, b in zip(digits[:12], ponderations)]
            remain = sum(terms) % 10
            check = 10 - remain if remain != 0 else 0
        return digits[-1] == check

    category_id = fields.Many2one('library.book.category', string='Category')

    #  чтобы страна издателя была в книжной форме.
    # дя этого используем вычисляемое поле на основе publisher_id,
    # значение которого будет принимать значение из поля country_id издателя.
    publisher_country_id = fields.Many2one(
        'res.country', string='Publisher Country',
        compute='_compute_publisher_country',
        # store = False, # Default is not to store in db
        # функция поиска для реализации логики поиска и
        # обратная функция для реализации логики записи.
        inverse='_inverse_publisher_country',
        search='_search_publisher_country',
    )

    # наше поле должно пересчитываться всякий раз,
    # когда изменяется country_id для publisher_id книги
    @api.depends('publisher_id.country_id')
    # функция вычисления страны издателя
    def _compute_publisher_country(self):
        for book in self:
            book.publisher_country_id = book.publisher_id.country_id

    @api.depends('publisher_country_id')
    def _inverse_publisher_country(self):
        for book in self:
            if book.publisher_id:
                book.publisher_id.country_id = book.publisher_country_id


    # поиск страны издателя
    def _search_publisher_country(self, operator, value):
        return [('publisher_id.country_id', operator, value)]

    publisher_country_related = fields.Many2one(
        'res.country',
        string='Publisher Country (related)',
        related='publisher_id.country_id',
    )

    # Ограничения SQL добавляются к определению таблицы базы данных и
    # применяются непосредственно PostgreSQL. Они определяются с помощью
    # атрибута класса _sql_constraints.
    _sql_constraints = [
        ('library_book_name_date_ug',
         'UNIQUE (name,date_published)',
         'Book title and publication date must be unique.'),
        ('library_book_check_date',
         'CHECK (date_published <= current_date)',
        'Publication date must not be in the future.'),
    ]

    # Ограничения Python могут использовать фрагмент произвольного кода для
    # проверки условий. Функция проверки должна быть украшена @ api.constrains
    # и указанием списка полей, участвующих в проверке. Проверка запускается при
    # изменении любого из них и вызывает исключение, если условие не выполняется.
    # предотвращение вставки неправильных номеров ISBN.
    @api.constrains('asbn')
    def _constrain_isbn_title(self):
        for book in self:
            if book.isbn and not book._check_isbn():
                raise ValidationError('%s is an invalid ISBN' % book.isbn)
