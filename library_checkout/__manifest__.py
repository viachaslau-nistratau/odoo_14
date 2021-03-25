# -*- coding: utf-8 -*-
{
    'name': "library_checkout",
    'description': 'Members can borrow books from the library.',
    'author': 'Daniel Reis',
    # добавляем почтовый модуль mail
    'depends': ['library_member', 'mail'],

    'data': [
        'security/ir.model.access.csv',
        'views/library_menu.xml',
        'views/checkout_view.xml',
        'views/library_checkout_stage.xml',
        'wizard/checkout_mass_message_wizard.xml',
    ],
}
