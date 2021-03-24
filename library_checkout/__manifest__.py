# -*- coding: utf-8 -*-
{
    'name': "library_checkout",
    'description': 'Members can borrow books from the library.',
    'author': 'Daniel Reis',
    'depends': ['library_member'],

    'data': [
        'security/ir.model.access.csv',
        'views/library_menu.xml',
        'views/checkout_view.xml',
    ],
}
