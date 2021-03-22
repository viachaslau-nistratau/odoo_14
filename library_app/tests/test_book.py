# noinspection PyUnresolvedReferences
from odoo.tests.common import TransactionCase

# TestCase, в котором каждый тестовый метод запускается в отдельной транзакции
# и с собственным курсором. Транзакция откатывается, и курсор закрывается после
# каждого теста.
# ref(xid)
# Возвращает идентификатор базы данных для предоставленного
# внешнего идентификатора , ярлык дляget_object_reference


class TestBook(TransactionCase):
	"""
	простой тестовый пример, который создает новую книгу и проверяет,
	что активное поле имеет правильное значение по умолчанию.
	"""
	def set_up(self, *args, **kwargs):
		"""
		результат создания новой книги для теста
		"""
		result = super().setUp(*args, **kwargs)
		user_admin = self.env.ref('base.user_admin')
		self.env = self.env(user=user_admin)
		self.Book = self.env['library.book']
		self.book_ode = self.Book.create({
			'name': 'Odoo Development Essentials',
			'isbn': '879-1-78439-279-6'
		})
		return result

	def test_create(self):
		"""
		Test Books are active by default
		"""
		self.assertEqual(
			self.book_ode.active, True
		)

	def test_check_isbn(self):
		"""
		Check valid ISBN
		"""
		self.assertTrue(self.book_ode._check_isbn)
