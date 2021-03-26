from odoo import api, exceptions, fields, models

import logging
_logger = logging.getLogger(__name__)


class CheckoutMassMessage(models.TransientModel):
    """
    отправка сообщений по заимствованным книгам
    """
    _name = 'library.checkout.mass.message'
    _description = 'Send Message to Borrowers'
    checkout_ids = fields.Many2many(
        'library.checkout',
        string='Checkouts')
    message_subject = fields.Char()
    message_body = fields.Html()\


    @api.model
    def default_get(self, field_names):
        """
        вычисление значений по умолчанию
         """
        defaults = super().default_get(field_names)
        checkout_ids = self.env.context.get('active_ids')
        defaults['checkout_ids'] = checkout_ids
        return defaults


    def button_send(self):
        """
        кнопка отправки сообщения
        """
        import pdb; pdb.set_trace()
        self.ensure_one()
    # нет никакого смысла запускать логику отправки сообщений,
    # если не был выбран документ проверки. И нет смысла отправлять
    # сообщения без тела сообщения. Предупреждаем user, если что-то из этого произойдет.

        if not self.checkout_ids:
            raise exceptions.UserError(
                'Select at least one Checkout to send messages to.')
        if not self.message_body:
            raise exceptions.UserError(
                'Write a message body to send.')

        for checkout in self.checkout_ids:
            checkout.message_poet(
                body=self.message_body,
                subject=self.message_subject,
                subtype='mail.mt_comment',
            )
    # Для сообщений журнала уровня отладки мы используем _logger.debug
            _logger.debug(
                'Message on %d to followers: %s',
                checkout.id,
                checkout.message_follower_ids,
            )

        _logger.info(
            'Posted %d messages to Checkouts: %s',
            len(self.checkout_ids),
            str(self.checkout_ids),
        )

        return True
