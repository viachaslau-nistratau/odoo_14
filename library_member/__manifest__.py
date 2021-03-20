# -*- coding: utf-8 -*-
{
    'name': 'Library Members',
    'description': 'Manage people who will be able to borrow books.',
    'author': 'Daniel Reis',
    'application': False,

    # Добавляем зависимость от дополнительного модуля, предоставив миксин Models: mail
    # нашему модулю расширения потребуется дополнительная почтовая зависимость.

    'depends': ['library_app', 'mail'],

    'date': [
        'security/ir.model.access.csv',
        'security/library_security.xml',
        'views/book_view.xml',
        'views/member_view.xml',
        'views/library_menu.xml',
        'views/book.list.template.xml',
    ],
}
