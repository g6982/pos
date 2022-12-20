import logging, re
import werkzeug

from odoo import http, _
from odoo.addons.auth_signup.models.res_users import SignupError
from odoo.addons.web.controllers.main import ensure_db, Home
from odoo.addons.base_setup.controllers.main import BaseSetup
from odoo.exceptions import UserError
from odoo.http import request


_logger = logging.getLogger(__name__)


class AuthSignupHome(Home):

	def do_signup(self, qcontext):
		""" Shared helper that creates a res.partner out of a token """
		num = request.env['ir.config_parameter'].sudo().get_param('odoo_user_login_security.number_of_question')
		number = num
		questions_lst = []
		answers_lst = []
		for i in range(int(number)):
			questions_lst.append('que_'+str(i+1))
			answers_lst.append('ans_'+str(i+1))
		values = { key: qcontext.get(key) for key in ('login', 'name', 'password') }
		questions = { key: qcontext.get(key) for key in questions_lst }
		answers = { key: qcontext.get(key) for key in answers_lst }
		lst_of_questions = list(questions.values())
		if not values:
			raise UserError(_("The form was not properly filled in."))
		if values.get('password') != qcontext.get('confirm_password'):
			raise UserError(_("Passwords do not match; please retype them."))
		if len(lst_of_questions) > 0:
			for val in lst_of_questions:
				if lst_of_questions.count(val) > 1:
					raise UserError(_("All the selected questions must be different."))
		supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
		lang = request.context.get('lang', '').split('_')[0]
		if lang in supported_lang_codes:
			values['lang'] = lang
		self._signup_with_values(qcontext.get('token'), values,questions,answers,questions_lst,answers_lst)
		request.env.cr.commit()

	def _signup_with_values(self, token, values,questions,answers,questions_lst,answers_lst):
		db, login, password = request.env['res.users'].sudo().signup(values, token)
		request.env.cr.commit()
		uid = request.session.authenticate(db, login, password)
		if not uid:
			raise SignupError(_('Authentication Failed.'))

		u_id = request.env['res.users'].sudo().search([('login','=',values['login'])])
		question_enabled = request.env['ir.config_parameter'].sudo().get_param('odoo_user_login_security.enable_security_question')
		if question_enabled:
			for rec in u_id:
				Line = [(5,0,0)]
				for i in range(len(questions_lst)):
					vals = {
						'question_id' : int(questions[questions_lst[i]]),
						'answer' : answers[answers_lst[i]],
						'user_id' : rec.id
					}
					Line.append((0, 0, vals))
				rec.line = Line


	@http.route('/update_question', type='http', auth='public', website=True, sitemap=False)
	def update_question(self, *args, **kw):
		qcontext = self.get_auth_signup_qcontext()
		users = request.env['res.users'].sudo().search([('id', '=', request.uid)])
		if kw.get('ans_1'):
			que = []
			ans = []
			for i in range(len(users.line.ids)):
				que.append('que_'+str(i+1))
				ans.append('ans_'+str(i+1))
			questions = { key: qcontext.get(key) for key in que }
			lst = list(questions.values())
			for val in lst:
				if lst.count(val) > 1:
					raise UserError(_("All the selected questions must be different."))
			for rec in users:
				Line = [(5,0,0)]
				for i in range(len(que)):
					vals = {
						'question_id' : int(kw.get(que[i])),
						'answer' : kw.get(ans[i]),
						'user_id' : rec.id
					}
					Line.append((0, 0, vals))
				rec.line = Line
			return http.request.render('odoo_user_login_security.updated',{})
		if len(users.line):
			return http.request.render('odoo_user_login_security.update_question',{'obj':users})
		else:
			raise Exception(_('No Question selected at time of signup!'))


	@http.route('/web/reset_password', type='http', auth='public', website=True, sitemap=False)
	def web_auth_reset_password(self, *args, **kw):
		qcontext = self.get_auth_signup_qcontext()
		question_enabled = request.env['ir.config_parameter'].sudo().get_param('odoo_user_login_security.enable_security_question')

		if not qcontext.get('token') and not qcontext.get('reset_password_enabled'):
			raise werkzeug.exceptions.NotFound()

		if 'error' not in qcontext and request.httprequest.method == 'POST':
			try:
				if qcontext.get('token'):
					self.do_signup(qcontext)
					return self.web_login(*args, **kw)
				else:
					login = qcontext.get('login')
					assert login, _("No login provided.")
					_logger.info(
						"Password reset attempt for <%s> by user <%s> from %s",
						login, request.env.user.login, request.httprequest.remote_addr)
					if kw.get('ans_1'):
						login = kw.get('login')
						users = request.env['res.users'].sudo().search([('login', '=', login)])
						i = 1
						for a in users.line:
							ans = 'ans_' + str(i)
							save_ans = a.answer
							save_ans = save_ans.split(' ')
							new_ans = kw.get(ans)
							new_ans = new_ans.split(' ')
							for rec in range(len(save_ans)):
								if save_ans[rec] != new_ans[rec]:
									raise Exception(_('Question and Answers does not match!'))
							i += 1
						request.env['res.users'].sudo().reset_password(login)
						qcontext['message'] = _("An email has been sent with credentials to reset your password")
					else:
						login = kw.get('login')
						users = request.env['res.users'].sudo().search([('login', '=', login)])
						if not users:
							users = request.env['res.users'].sudo().search([('email', '=', login)])

						if not users:
							raise Exception(_('Reset password: invalid username or email!'))
						if len(users.line) and question_enabled:
							ren_temp = request.render('odoo_user_login_security.reset_question_answer', {'obj':users})
							return ren_temp
						else:
							request.env['res.users'].sudo().reset_password(login)
							qcontext['message'] = _("An email has been sent with credentials to reset your password")

			except UserError as e:
				qcontext['error'] = e.name or e.value
			except SignupError:
				qcontext['error'] = _("Could not reset your password")
				_logger.exception('error when resetting password')
			except Exception as e:
				qcontext['error'] = str(e)


		response = request.render('auth_signup.reset_password', qcontext)
		response.headers['X-Frame-Options'] = 'DENY'
		return response

	@http.route('/web/update_que_ans', type='json', auth='public', website=True, sitemap=False)
	def update_que_ans(self, fields):
		users = request.env['res.users'].sudo().search([('id', '=', request.uid)])

		if not len(users.line):
			raise UserError(_('No Question selected at time of signup!'))

		number = request.env['ir.config_parameter'].sudo().get_param('odoo_user_login_security.number_of_question')
		lst = []
		i = 0
		question = []
		answer = []
		for data in fields:
			que = 'que_'+str(i+1)
			if data['name'] == que:
				question.append(int(data['value']))
				i += 1
				if question.count(int(data['value'])) > 1:
					raise UserError(_("All the selected questions must be different."))
			else:
				answer.append(data['value'])

		for rec in users:
			Line = [(5,0,0)]
			for i in range(len(question)):
				vals = {
					'question_id' : int(question[i]),
					'answer' : answer[i],
					'user_id' : rec.id
				}
				Line.append((0, 0, vals))
			rec.line = Line

		return True

