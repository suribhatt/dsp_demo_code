# -*- coding: utf-8 -*-

import logging

from odoo import api, models

_logger = logging.getLogger(__name__)


class DsPayment(models.TransientModel):
    _name = "ds.payment"

    @api.model
    def set_odoo_order_paid(self, amount, order_id, journal_id):
        """Make the order Paid in Odoo"""
        status = True
        draftInvoiceId = 0
        invoiceId = False
        statusMessage = "Payment Successfully made for Order."
        try:
            journalId = journal_id
            saleObj = self.env['sale.order'].browse(
                int(order_id))
            if not saleObj.invoice_ids:
                invoiceId = self.create_odoo_order_invoice(int(order_id))
                if invoiceId:
                    draftInvoiceId = invoiceId
            elif saleObj.invoice_ids:
                for invoiceObj in saleObj.invoice_ids:
                    if invoiceObj.state == 'posted':
                        invoiceId = invoiceObj.id
                    elif invoiceObj.state == 'draft':
                        draftInvoiceId = invoiceObj.id
            if draftInvoiceId:
                invoiceId = draftInvoiceId
                invoiceObj = self.env[
                    'account.move'].browse(invoiceId).action_post()
            register_wizard = self.env['account.payment.register'].with_context({
                'active_model': 'account.move',
                'active_ids': [invoiceId]
            })
            _logger.info("================journalId===============%r",(journal_id, amount, order_id))
            register_wizard_obj = register_wizard.create({
                'journal_id': journalId,
                'amount': float(amount)
            })
            register_wizard_obj.action_create_payments()
        except Exception as e:
            statusMessage = "Error in creating Payments for Invoice: %s" % str(
                e)
            _logger.debug('## Exception set_order_paid for sale.order(%s) : %s' % (order_id, statusMessage))
            status = False
        finally:
            return {
                'status_message': statusMessage,
                'status': status
            }

    @api.model
    def create_odoo_order_invoice(self, orderId):
        """Create Invoice For Order
        """
        invoiceId = False
        try:
            saleObj = self.env['sale.order'].browse(orderId)
            invoiceId = saleObj.invoice_ids
            if saleObj.state == 'draft':
                self.confirm_odoo_order(orderId)
            if not invoiceId:
                invoiceId = saleObj._create_invoices()
        except Exception as e:
            statusMessage = "Error in creating Invoice: %s" % str(e)
            _logger.debug('## Exception create odoo order invoice for sale.order(%s) : %s' % (orderId, statusMessage))
        finally:
            if invoiceId:
                invoiceId = invoiceId[0].id
            else:
                invoiceId = 0
            return invoiceId
    
    @api.model
    def confirm_odoo_order(self, order_id):
        """ Confirm Odoo Order"""
        status = True
        status_message = "Order Successfully Confirmed!!!"
        try:
            saleObj = self.env['sale.order'].browse(order_id)
            saleObj.action_confirm()
        except Exception as e:
            status_message = "Error in Confirming Order on Odoo: %s" % str(e)
            _logger.debug('#Exception confirm_odoo_order for order(%s) : %s' % (order_id, status_message))
            status = False
        finally:
            return {
                'status': status,
                'status_message': status_message
            }
    