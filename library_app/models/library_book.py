# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError
import re

BOOK_STATUS_WANTED = 'wanted'
BOOK_STATUS_IN_PROGRESS = 'in_the_process'
BOOK_STATUS_DONE = 'done'


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
    # а затем в обратном порядке дата публикации (от самой новой до самой
    # старой)

    _order = 'name, date_published desc'

    # _order устанавливает порядок по умолчанию для использования
    # при просмотре записей модели, или отображается в виде списка.

    # Text fields
    # использование аргументов ключевого слова для атрибутов поля:

    name = fields.Char(
        string='Название книги',
        size=35,
    )
    # requered = True,
    """
    дополнительные атрибуты - default=None, index=True, help='Book cover title', 
    readonly=False, required=True, translate=False,
    """

    # String fields: name = fields.Char('Title')
    # Char (string) - это одна строка текста.
    # Единственный ожидаемый позиционный аргумент: метка строкового поля

    isbn = fields.Char(
        string='ISBN',
    )

    # Selection (selection, string) - это раскрывающийся список выбора.
    # Выбор позиционных аргументов - это список кортежей [('value', 'Title'),].
    # Первый элемент кортежа - это значение, хранящееся в базе данных.
    # Второй элемент кортежа - это описание представленое в пользовательском
    # интерфейсе. Этот список может быть расширен другими модулями, используя
    # аргумент ключевого слова selection_add.

    book_type = fields.Selection(
        [('paper', 'мягкая обложка'),
         ('hard', 'твердый переплет'),
         ('electronic', 'электронная книга'),
         ('other', 'прочее')],
        'Тип',
    )

    # Html хранится как текстовое поле, но имеет специфическую обработку
    # пользователя интерфейса для представления содержимого HTML
    # descr = fields.Html('Description')
    # Numeric fields
    # Integer (string) просто ожидает строковый аргумент для заголовка поля.
    # copies = fields.Integer(default=1)
    # Float (string, digits) имеет второй необязательный аргумент - цифры,
    # как (x, y) кортеж с точностью поля. x - общее количество цифр; из них
    # y десятичные цифры.
    # avg_rating = fields.Float('Average Rating', (3, 2))
    # Monetary (string, currency_field) похоже на поле с плавающей запятой,
    # но имеет особую обработку валюты. Используется второй аргумент
    # currency_field для установки поля, в котором хранится используемая
    # валюта. По умолчанию ожидается поле currency_id.
    # price = fields.Monetary('Price', 'currency_id')
    # currency_id = fields.Many2one('res.currency')
    # Date and time fields
    # Date (string) и Datetime(string) ожидают только текст строки как
    # позиционный аргумент.
    # вычисление значения по умолчанию с текущими датой и временем:

    last_borrow_date = fields.Datetime(
        'Last Borrowed One',
        default=lambda self: fields.Datetime.now(),
    )

    # Other fields
    # Boolean(string) содержит значения True или False, как и следовало
    # ожидать, и имеет только один позиционный аргумент для текстовой строки.

    active = fields.Boolean('Available?', default=True)

    # Binary(string) хранит двоичные данные в виде файлов, а также ожидает
    # только строку аргумент. может быть обработано кодом Python с
    # использованием строк в кодировке base64.

    image = fields.Binary(
        string='Обложка книги',
    )

    # Relation fields
    # поле publisher_id представляет издателя книги и является
    # ссылкой на запись в партнерской модели

    publisher_id = fields.Many2one(
        comodel_name='res.partner',
        string='Издательство',
    )

    # связь "многие ко многим" между книгами и авторами: у каждой книги
    # может быть много авторов, и у каждого автора может быть много книг

    # Date and time fields
    # Date (string) и Datetime(string) ожидают только текст строки как
    # озиционный аргумент.

    author_ids = fields.One2many(
        comodel_name='res.partner',
        inverse_name='book_ids',
        string='Автор',
    )

    #  чтобы страна издателя была в книжной форме.
    # дя этого используем вычисляемое поле на основе publisher_id,
    # значение которого будет принимать значение из поля country_id издателя.

    publisher_country_id = fields.Many2one(
        comodel_name='res.country', string='Publisher Country',
        compute='_compute_publisher_country',
        # store = False, # Default is not to store in db
        # функция поиска для реализации логики поиска и
        # обратная функция для реализации логики записи.
        inverse='_inverse_publisher_country',
        search='_search_publisher_country',
    )

    category_id = fields.Many2many(
        comodel_name='library.book.category',
        string='Жанр книги',
    )

    add_info = fields.Char(
        string='Автор/Название книги/Год издания',
        compute='_compute_name_author',
        readonly=False,
    )
        # inverse='_set_name_author',)

    count_page = fields.Integer(
        string='Количество страниц',
    )

    BOOK_STATUS = [
        (BOOK_STATUS_WANTED, 'Хочу прочитать'),
        (BOOK_STATUS_IN_PROGRESS, 'Читаю'),
        (BOOK_STATUS_DONE, 'Книга прочитана'),
    ]

    status_book = fields.Selection(
        BOOK_STATUS,
        string='статус книги',
        default=BOOK_STATUS_WANTED,
    )

    # checkbox (флажки) вызова дополнительной информации
    check_button = fields.Boolean(
        string='Доп. информация'
    )
    # тесктовое поле не имеет размера
    notes = fields.Text(
        string='Краткое содержание'
    )
    check_button_notes = fields.Boolean(
        string='Примечание'
    )

    info_member_take_book = fields.Boolean(
        string='Информация о пользователе, взявшем книгу'
    )
    member_book_id = fields.Many2one(
        comodel_name='library.member',
        string='ФИО',
    )

    date_published = fields.Char(
        string='Год издания',
        size=4,
    )

    @api.depends('author_ids.name')
    def _compute_name_author(self):
        """
        функция конкатенции 3-х полей - автора, названия книги и даты публикации
        второй вариант когда дата - всего лишь год
        """
        for book in self:
            name_book = book.name
            author = book.author_ids.name
            if book.date_published:
                year = book.date_published
            else:
                year = 'Год издания не известен'
            book.add_info = f'{author} - {name_book} ({year})'

    # @api.depends('author_ids.name')
    # def _compute_name_author(self):
    #     for book in self:
    #         name_book = book.name
    #         author_names = book.author_ids.mapped('name')

    # def some_name_author(self):
    #     """
    #     модуль ввода нескольких авторов
    #     """
    #     for book in self:
    #          name_book = book.name
    #          author_names = book.author_ids.mapped('name')


    #         # todo : еще одна переменная с именем автор в которую нужно
    #         #  получить строку с именами авторов из переменнной author_names
    #         # в дебаге или принтом смотреть что туда приходит (значения)

    date_start_read = fields.Date(
        string='Начало чтения',
    )
    date_finish_read = fields.Date(
        string='Окончание чтения',
    )

    def start_read_book(self):
        """
        меняется статус книги на 'читаю', дата начала чтения книги
        :return: True - результат записи - смены статуса книги
        """
        self.write({
            'status_book': BOOK_STATUS_IN_PROGRESS,
            'date_start_read': fields.Date.today(),
        })
        return True

    def finish_read_book(self):
        """
        меняется статус книги на 'прочитано', дата окончания чтения книги
        :return: True - результат записи - смены статуса книги
        """
        self.write({
            'status_book': BOOK_STATUS_DONE,
            'date_finish_read': fields.Date.today(),
        })
        return True

    # def double_check_book(self):
    #     """
    #     модуль проверки на дублирование названия книги
    #     при создании новой записи в библиотеке
    #     """
    #     for book in self:
    #         if book.name ==

    def button_check_isbn(self):
        """
        использование  функции _check_isbn для проверки isbn
        """
        for book in self:
            if not book.isbn:
                raise ValidationError('Пожалуйста укажите ISBN для %s'
                                      % book.name)
            if book.isbn and not book._check_isbn():
                raise ValidationError(f'{book.isbn} это неправильный ISBN')
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
            # check = 10 - remain if remain != 0 else 0
            check = 10 - remain if remain != 0 else 0
        return digits[-1] == check

    def compliance_check_isbn(self, vals):
        """
        проверка соответствия введенного ISBN - шаблону,
        с использованием регулярных выражений
        """
        if 'isbn' in vals:
            isbn_value = vals.get('isbn', '')
            # формат ISBN (примерный) 1-111-11111-1
            pattern_one = r'\b(\d)([-]{1})(\d{3})([-]{1})(\d{5})([-]{1})(\d)'
            result_one = re.match(pattern_one, isbn_value)
            # формат ISBN (примерный) 111-1-11111-111-1
            pattern_two = r'\b(\d{3})([-]{1})(\d)([-]{1})(\d{5})([-]{1})(\d{3})([-]{1})(\d)'
            result_two = re.match(pattern_two, isbn_value)
            if not result_one or not result_two:
                raise ValidationError(f'{isbn_value} это неправильный ISBN')

    # @ api.depends (fld1, ...) используется для вычисляемых функций поля,
    # чтобы определить, при каких изменениях (повторное) вычисление должно
    # запускаться. Он должен устанавливать значения в вычисленных полях,
    # иначе произойдет ошибка. наше поле должно пересчитываться всякий раз,
    # когда изменяется country_id для publisher_id книги

    # функция вычисления страны издателя

    @api.depends('publisher_id.country_id')
    def _compute_publisher_country(self):
        for book in self:
            book.publisher_country_id = book.publisher_id.country_id

    @api.depends('publisher_country_id')
    def _inverse_publisher_country(self):
        for book in self:
            if book.publisher_id:
                book.publisher_id.country_id = book.publisher_country_id

    # поиск страны издателя
    @staticmethod
    def _search_publisher_country(operator, value):
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
         'Publication date must not be in the future.'
         ),
    ]

    # Ограничения Python могут использовать фрагмент произвольного кода для
    # проверки условий. Функция проверки должна быть украшена @ api.constrains
    # и указанием списка полей, участвующих в проверке. Проверка запускается
    # при изменении любого из них и вызывает исключение, если условие не
    # выполняется. предотвращение вставки неправильных номеров ISBN.

    def write(self, vals):
        """
        модуль запуска автоматической проверки isbn при сохранении записи
        """
        self.compliance_check_isbn(vals)
        res = super(Book, self).write(vals)
        return res
