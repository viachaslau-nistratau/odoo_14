from odoo import api, fields, models


class BookCategory(models.Model):
    """
    категории книг
    """
    _name = 'library.book.category'
    _description = 'Book Category'
    #  для того чтобы включить индексацию иерархии и
    #  ускорить поиск в дереве, добавляем атрибут модели _parent_store = True.
    _parent_store = True

    name = fields.Char(translate=True, required=True)
    # Hierarchy fields
    # поле parent_id для ссылки на родительскую запись.
    parent_id = fields.Many2one(
        'library.book.category',
        'Parent Category',
        ondelete='restrict',
    )

    # вспомогательное поле parent_path, должно быть проиндексировано,
    # хранится дополнительная информация о древовидной структуре иерархии,
    # которая используется для более быстрых запросов.
    parent_path = fields.Char(index=True)

    # Optional but good to have:
    child_ids = fields.One2many(
        'library.book.category',
        'parent_id',
        'Subcategories',
    )

    # добавление ссылки на выделенную книгу или автора.
    # поле может относиться либо к книге, либо к партнеру
    # тип поля ссылка (Reference)
    highlighted_id = fields.Reference(
        [('library.book', 'Book'),
         ('res_partner', 'Author')],
        'Category Highlight',
    )
