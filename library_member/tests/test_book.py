from odoo.tests.common import TransactionCase


class TestBook(TransactionCase):

    def test_check_isbn10(self):
        """
        check valid ISBN10
        """
        book = self.env['library.book']
        book = book.create({
            'name': 'The Pythons: Autobiography by the Pythons',
            'isbn': '0312311443',
        })
        self.assertTrue(book.__check_isbn)
