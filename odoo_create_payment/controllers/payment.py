# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request


class PaymentController(http.Controller):

    @http.route(['/create_payments'], type='json', auth="public", cors='*')
    def create_payments(self, amount, order_id, journal_id):
        """Make the order Paid in Odoo From Json-rpc api"""
        status = True
        statusMessage = ''
        if not (amount or order_id or journal_id):
            status = False
            statusMessage = "Please provide amount, order_id and journal_id"
        else:
            if amount==0:
                status = False
                statusMessage = "Amount should be greater than 0"
            return request.env['ds.payment'].set_odoo_order_paid(amount, order_id, journal_id)
        return {
            'status_message': statusMessage,
            'status': status
        }