from odoo import models, fields,api,exceptions
from datetime import datetime,date
import logging
_logger = logging.getLogger(__name__)

class SecurityQuestion(models.Model):
	_name = "res.security.question"

	name = fields.Char(string = "Question")
	# archive = fields.Boolean(string='Archive')
	active = fields.Boolean('Active', default=True)


class SecurityAnswer(models.Model):
	_name = "res.security.answer"

	question_id = fields.Many2one('res.security.question',string = "Question")
	answer = fields.Char(string = "Answer")
	user_id = fields.Many2one('res.users')

class FieldsInherit(models.Model):
	_inherit = 'res.users'

	line = fields.One2many(comodel_name='res.security.answer',inverse_name='user_id')

	def update_que_ans(self):
		num_que = self.env['ir.config_parameter'].sudo().get_param('odoo_user_login_security.number_of_question')
		enable = self.env['ir.config_parameter'].sudo().get_param('odoo_user_login_security.enable_security_question')
		questions = self.env['res.security.question'].search([])

		num_que = [i for i in range(int(num_que))]
		ques = [{'id':que.id,'name':que.name} for que in questions]
		return {
			'type': 'ir.actions.client',
			'tag': 'update_que_ans',
			'target': 'new',
			'params': {'num_of_que': num_que,'questions': ques,'enable': enable}
		}
