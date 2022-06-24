# -*- coding: utf-8 -*-

from odoo import fields, models


class Office365MessageWizard(models.TransientModel):
	_name = "office365.message.wizard"
	_description = "Message Wizard For Office365 View"
	
	text = fields.Text(string='Message', readonly=True, translate=True)

	def generate_message(self, message, name='Message/Summary'):
		partial_id = self.create({'text':message}).id
		return {
			'name':name,
			'view_mode': 'form',
			'view_id': False,
			'res_model': 'office365.message.wizard',
			'res_id': partial_id,
			'type': 'ir.actions.act_window',
			'nodestroy': True,
			'target': 'new',
			'domain': '[]',
		}
