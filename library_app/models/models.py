from odoo import fields, models
# импорт объектов модулей и полей


class Book(models.Model): # новая модель
	_name = 'library.book'
    # атрибут _name, определяющий идентификатор,
    # который будет использоваться повсюду Odoo для обозначения этой модели
	_description = 'Book'
    # атрибут модели _description обеспечивает
    # удобное имя для записей модели, которое можно использовать для улучшения
    # пользовательских сообщений. Остальные строки определяют поля модели.
	name = fields.Char('Title', required=True)
	isbn = fields.Char('ISBN')
	active = fields.Boolean('Active?', default=True)
	date_published = fields.Date()
	image = fields.Binary('Cover')
	publisher_id = fields.Many2one('res.partner', string='Publisher')
	author_ids = fields.Many2many('res.partner', string='Authors')



# from odoo import models, fields, api


# class library_app(models.Model):
#     _name = 'library_app.library_app'
#     _description = 'library_app.library_app'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
