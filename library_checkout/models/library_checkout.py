from odoo import api, exceptions, fields, models


class Checkout(models.Model):
    """
    модуль выбора книг (запроса)
    """
    _name = 'library.checkout'
    _description = 'Checkout Request'
    # наследование от абстрактных моделей миксинов
    _inherit = ['mail.thread', 'mail.activity.mixin']

    def name_get(self):
        names = []
        for rec in self:
            name = '%s/%s' % (rec.member_id, rec.request_date)
            names.append((rec.id, name))
        return names

    """
    иногда необходимо, чтобы метод работал на уровне класса, а не с
    конкретными записями. Это называется статическим методом. Эти
    статические методы уровня класса должны быть украшены @ api.model.
    В этих случаях self следует использовать в качестве ссылки для модели,
    не ожидая, что она будет содержать фактические записи.
    """

    @api.model
    def _default_stage(self):
        stage = self.env['library.checkout.stage']
        return stage.search([], limit=1)

    # в книге есть параметр domain, в коде он не виден - разобраться
    # def _group_expand_stage_id(self, stages, domain, order):

    @api.model
    def _group_expand_stage_id(self, stages, order):
        return stages.search([], order=order)

    member_id = fields.Many2one(
        comodel_name='library.member',
        string='Member',
        required=True,
    )
    user_id = fields.Many2one(
        'res.users',
        string='Librarian',
        default=lambda s: s.env.uid,
    )
    request_date = fields.Date(
        default=lambda s: fields.Date.today())
    line_ids = fields.One2many(
        'library.checkout.line',
        'checkout_id',
        string='Borrowed Books',
    )

    # модель этапов запроса книг.
    # Значение стадии по умолчанию вычисляется вспомогательной функцией
    # _default_stage (), которая возвращает первую запись в модели стадий.
    # Поскольку сценическая модель правильно упорядочена по последовательности,
    # она вернет модель с наименьшим порядковым номером.
    # Параметр group_expand переопределяет способ работы группировки по полю.
    # По умолчанию и ожидаемое поведение для операций группирования заключается
    # в том, чтобы видеть только используемые этапы, а этапы без документа
    # проверки не отображаются. Но в этом случае мы бы предпочли что-то другое;
    # мы хотели бы видеть все доступные этапы, даже если на них нет документов.
    # Вспомогательная функция _group_expand_stage_id () возвращает список
    # записей группы, которые должна использовать операция группировки.

    stage_id = fields.Many2one(
        'library.checkout.stage',
        default=_default_stage,
        group_expand='_group_expand_stage_id',
    )

    # поле состояния. Это связанное (related) поле, которое
    # просто делает доступным поле (state) состояния стадии в этой модели

    state = fields.Selection(related='stage_id.state')

    # добавим два поля даты, чтобы записывать, когда проверка перешла
    # в открытое состояние и когда она перешла в закрытое состояние.

    # checkout_date = fields.Date(readonly=True)
    # closed_date = fields.Date(readonly=True)
    checkout_date = fields.Date()
    closed_date = fields.Date()

    # автоматизации в форме оформления заказа - когда абонент библиотеки
    # изменяется, дата запроса устанавливается на сегодняшний день, и
    # пользователю показывается предупреждающее сообщение, предупреждающее его
    # об этом Внутри метода onchange self представляет собой одну виртуальную
    # запись, содержащую все поля, которые в настоящее время установлены в
    # редактируемой записи, и мы можем взаимодействовать с ними. В большинстве
    # случаев это то, что мы хотим сделать, чтобы автоматически заполнять
    # значения в других полях, в зависимости от значения, установленного для
    # измененного поля. В этом случае мы обновляем поле request_date до
    # сегодняшнего дня. Методы onchange ничего не должны возвращать, но они
    # могут возвращать словарь, содержащий предупреждение или ключ домена

    @api.onchange('member_id')
    def onchange_member_id(self):
        """
        функция изменения абонента библиотеки
        """
        today = fields.Date.today()
        if self.request_date != today:
            self.request_date = fields.Date.today()
            return {
                'warning': {
                    'title': 'Changed Request Date',
                    'message': 'request date changed to today.',
                }
            }

    # создаем собственный метод create (), чтобы установить checkout_date,
    # если он находится в соответствующем состоянии, и предотвратить создание
    # проверок в состоянии «Готово»
    # При использовании Python 3 доступен упрощенный способ использования
    # super()
    # В Python 2 мы бы написали super (Checkout, self) .create (vals),
    # где checkout - имя класса Python, в котором мы находимся.
    # Это все еще действующий синтаксис для Python 3, но у нас также есть новый
    # упрощенный синтаксис: super (). create (vals).
    # new_record = super(Checkout, self).create(vals)

        @api.model
        def create(self, vals):
            """
            Code before create: should use the `vals` dict
            """
            if 'stage_id' in vals:
                stage = self.env['library.checkout.stage']
                new_state = stage.browse(vals['stage_id']).state
                if new_state == 'open':
                    vals['checkout_date'] = fields.Date.today
            new_record = super().create(vals)
            # Code after create: can use the `new_record` created
            if new_record.state == 'done':
                raise exceptions.UserError(
                    'Not allowed to create a checkout in the done state.')
            return new_record

    # специальный метод для выполнения некоторых действий с набором записей
    # - @ api.multi,и в этом случае аргумент self будет набором записей,
    # с которым мы будем работать.
    # Логика метода обычно включает в себя итерацию цикла for.

    # когда запись изменяется, мы хотим обновить checkout_date и close_date,
    # если запись выбора переходит в соответствующие состояния.
    # Для этого у нас будет собственный метод write ()
    # В этом методе наша конкретная логика защищена оператором if и запускается
    # только в том случае, если определенный маркер не найден в контексте.
    # Кроме того, наши операции self.write () должны использовать with_context
    # для установки этого маркера. Эта комбинация гарантирует, что
    # пользовательский вход внутри оператора if запускается только один раз и
    # не запускается при последующих вызовах write (), избегая
    # бесконечного цикла.

    # разобраться почему ОДОО14 ругается на декоратор @api.multi
    # @api.multi
    def write(self, vals):
        """
        функция
        """
        if 'stage_id' in vals:
            """
            Code before write: can use self, with the old values
            """
            stage = self.env['library.checkout.stage']
            new_state = stage.browse(vals['stage_id']).state
            if new_state == 'open' and self.state != 'open':
                vals['checkout_date'] = fields.Date.today()
            if new_state == 'done' and self.state != 'done':
                vals['close_date'] = fields.Date.today()
        super().write(vals)
        # Code after write: can use self, with the updated values
        return True

    # сделаем изображение абонента библиотеки доступным в документе оформления
    # заказа
    # member_image = fields.Binary(related='member_id.partner_id.image')
    num_other_checkouts = fields.Integer(
        compute='_compute_num_other_checkouts'
    )

    def _compute_num_other_checkouts(self):
        for rec in self:
            domain = [
                ('member_id', '=', self.member_id.id),
                ('state', 'in', ['open']),
                ('id', '!=', rec.id)]
            return self.search_count(domain)

    num_books = fields.Integer(
        compute='_compute_num_books',
        store=True)

    @api.depends('line_ids')
    def _compute_num_books(self):
        for book in self:
            book.num_books = len(book.line_ids)



    def button_done(self):
        """
        метод вызова кнопки - Возврат книг находит запись этапа done для
        использования, а затем для каждой записи в собственном наборе записей
        устанавливает для этого stage_id значение этапа done
        """
        stage = self.env['library.checkout.stage']
        done_stage = stage.search(
            [('state', '=', 'done')],
            limit=1)
        for checkout in self:
            checkout.stage_id = done_stage
        return True


class CheckoutLine(models.Model):
    """
    модуль проверки выбора книг (запроса)
    """
    _name = 'library.checkout.line'
    _description = 'Borrow Request Line'

    checkout_id = fields.Many2one('library.checkout')
    book_id = fields.Many2one('library.book')
