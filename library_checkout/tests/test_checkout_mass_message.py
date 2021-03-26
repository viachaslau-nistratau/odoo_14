from odoo.tests.common import TransactionCase
from odoo import exceptions


class TestWizard(TransactionCase):
    """
    создание логики для wizard. TransactionCase для каждого теста
    используются разные транзакции,
    которые в конце автоматически откатываются
    """
    def set_up(self, *args, **kwargs):
        """
        создание контрольной записи для использования в wizard
        """
        super(TestWizard, self).set_up(*args, **kwargs)
        # Setup test data
        admin_user = self.env.ref('base.user_admin')
        self.Checkout = self.env['library.checkout'].sudo(admin_user)
        self.Wizard = self.env['library.checkout.mass.message'].sudo(admin_user)

        a_member = self.env['library.member'].create({'name': 'John'})
        self.checkout0 = self.Checkout.create({'member_id': a_member.id})

    # Add test setup code here...
    def test_button_send(self):
        """Send button should create messages on Checkouts"""
        # Add test code
        msgs_before = len(self.checkout0.message_ids)

        wizard0 = self.wizard.with_context(active_ids=self.checkout0.ids)
        wizard0 = wizard0.create({'message_body': 'Hello'})
        wizard0.button_send()

        msgs_after = len(self.checkout0.message_ids)
        self.assertEqual(
            msgs_after,
            msgs_before + 1,
            'Expected one additional message in the Checkout.'
        )

    def test_button_send_empty_body(self):
        'Send button errors on empty body message.'
        wizard0 = self.Wizard.create({})
        with self.assertRaises(exceptions.UserError) as e:
            wizard0.button_send()
