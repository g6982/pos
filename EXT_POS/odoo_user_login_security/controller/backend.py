# -*- coding: utf-8 -*-
##############################################################################
# Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# See LICENSE file for full copyright and licensing details.
# License URL : <https://store.webkul.com/license.html/>
##############################################################################
from odoo import fields,http
from odoo.http import request
import logging, datetime, calendar
from calendar import monthrange
_logger = logging.getLogger(__name__)


browser_logo_files = {
	'chrome' : 'chrome.png',
	'edge'   : 'edge.png',
	'firefox': 'firefox.png',
	'msie'   : 'msie.png',
	'opera'  : 'opera.png',
	'safari' : 'safari.png',
}
platform_logo_files = {
	'android' : 'android.png',
	'chromeos': 'chromeOS.png',
	'ipad'    : 'ipad.png',
	'iphone'  : 'iphone.png',
	'linux'   : 'linux.png',
	'macos'   : 'macos.png',
	'windows' : 'windows.png',
	'other'   : 'browser.png',
}
logo_file ='/odoo_user_login_security/static/src/img/'


class WebsiteBackend(http.Controller):
	@http.route('/session/fetch_dashboard_data',type="json",auth='user')
	def fetch_dashboard_data(self,tz,**kw):
		browser_selections  = dict(request.env['session.session']._fields.get('browser').selection)
		platform_selections = dict(request.env['session.session']._fields.get('platform').selection)

		recent_sessions = request.env['session.session'].search_read(
			domain = [],
			fields = ['id','browser','date_login','ip','platform','user_id'],
			limit  = 5,
			order  = 'date_login desc',
		)
		for session in recent_sessions:
			browser  = session.get('browser')
			platform = session.get('platform')

			date_login = fields.Datetime.context_timestamp(
				request.env.user.with_context(tz=tz),
				session.get('date_login'),
			).replace(tzinfo=None)

			browser_logo_file = logo_file + browser_logo_files.get(browser,'browser.png')
			platform_logo_file = logo_file + platform_logo_files.get(platform,'browser.png')

			session.update(
				date_login    = date_login,
				user          = session.pop('user_id')[1],
				platform_name = platform_selections.get(platform),
				browser_name  = browser_selections.get(browser),
				browser_logo  = browser_logo_file,
				platform_logo = platform_logo_file,
			)

		browser_sessions = []
		sessions = request.env['session.session'].search(
			[
				'|',
				('active','=',True),
				('active','=',False),
			]
		)
		for browser,label in browser_selections.items():
			all_sessions = sessions.filtered(lambda self: self.browser == browser)
			active_sessions = all_sessions.filtered(lambda self: self.active == True)
			browser_logo_file = logo_file + browser_logo_files.get(browser,'browser.png')
			platform_logo_file = logo_file + platform_logo_files.get(browser,'browser.png')
			browser_sessions.append(
				{
					'browser'      : browser,
					'browser_name' : label,
					'total_count'  : len(all_sessions),
					'active_count' : len(active_sessions),
					'browser_logo' : browser_logo_file,
					'platform_logo': platform_logo_file,
				}
			)
		browser_sessions = sorted(
			browser_sessions,
			key=lambda k:(k['browser']=='other',k['browser'])
		)

		state_counts = []
		for state,label in sessions._fields.get('state').selection:
			state_counts.append(
				{
					'state' : state,
					'status': label,
					'count' : len(sessions.filtered(lambda self:self.state == state)),
				}
			)

		return {
			'browser_sessions': browser_sessions,
			'recent_sessions' : recent_sessions,
			'state_counts'    : state_counts,
		}

	@http.route('/session/get_dashboard_line_data',type = 'json', auth = 'user')
	def get_dashboard_line_data(self,tz,days,**kw):
		labels = []
		lst = []
		today = fields.date.today()
		if days == 7 or days == 30:
			if days == 7:
				if today.day < 7:
					pre_month = monthrange(today.year,(today.month)-1 if today.month > 1 else 12)
					pre_month = pre_month[1]
					strt_date = 6 - today.day
					strt_date = pre_month - strt_date
					mnth = (today.month)-1 if today.month > 1 else 12
					year = (today.year) if today.month > 1 else (today.year) - 1
					for i in range(7):
						d = str(strt_date)+'/'+str(mnth)
						lst_d = (strt_date,mnth,year)
						lst.append(str(lst_d))
						labels.append(d)
						if strt_date == pre_month:
							strt_date = 0
							mnth = today.month
							if year < today.year:
								year += 1
						strt_date += 1
				else:
					strt_date = today.day -6
					for i in range(7):
						d = str(strt_date)+'/'+str(today.month)
						lst_d = (strt_date,today.month, today.year)
						lst.append(str(lst_d))
						labels.append(d)
						strt_date += 1
			else:
				if today.day < 30:
					pre_month = monthrange(today.year,(today.month)-1 if today.month > 1 else 12)
					pre_month = pre_month[1]
					strt_date = 29 - today.day
					strt_date = pre_month - strt_date
					mnth = (today.month)-1 if today.month > 1 else 12
					year = (today.year) if today.month > 1 else (today.year) - 1
					for i in range(30):
						d = str(strt_date)+'/'+str(mnth)
						labels.append(d)
						lst_d = (strt_date,mnth,year)
						lst.append(str(lst_d))
						if strt_date == pre_month:
							strt_date = 0
							mnth = today.month
							if year < today.year:
								year += 1
						strt_date += 1
				else:
					strt_date = today.day - 29
					for i in range(30):
						d = str(strt_date)+'/'+str(today.month)
						labels.append(d)
						lst_d = (strt_date,today.month, today.year)
						lst.append(str(lst_d))
						strt_date += 1
		else:
			strt_mnth = today.month + 1
			yr = today.year - 1
			if strt_mnth > 12:
				strt_mnth = 1
				yr += 1
			lst_d = []
			for i in range(12):
				mnth = calendar.month_abbr[strt_mnth]
				lst_d = (strt_mnth,yr)
				lst.append(str(lst_d))
				d = str(mnth)+'/'+str(yr)
				if strt_mnth == 12:
					yr += 1
					strt_mnth = 0
				strt_mnth += 1
				labels.append(d)



		sessions = request.env['session.session'].search([
			'|',
			('active','=',True),
			('active','=',False),
		])
		tst_date = []
		count_dict = {i:[] for i in lst}

		for rec in sessions:
			login = rec.date_login
			logout = rec.date_logout
			d_login1 = str((login.month,login.year))
			d_login = str((login.day,login.month,login.year))
			d_logout1 = ''
			d_logout = ''
			if logout:
				d_logout1 = str((logout.month,logout.year))
				d_logout = str((logout.day,logout.month,logout.year))
			if d_login in lst or d_logout in lst:
				tst_date.append(rec)
				if d_login in lst:
					count_dict[d_login].append(rec)
				else:
					count_dict[d_logout].append(rec)
			if d_login1 in lst or d_logout1 in lst:
				tst_date.append(rec)
				if d_login1 in lst:
					count_dict[d_login1].append(rec)
				else:
					count_dict[d_logout1].append(rec)

		data = {'labels':labels,
			'datasets':[]}


		login_fail = {
				'label': 'Login Fail',
				'data': [],
				'fill': False,
				'borderColor': 'rgb(255, 51, 0)',
				'backgroundColor': 'rgb(255, 51, 0)',
				'tension': 0.1
			}

		terminate = {
				'label': 'Terminate',
				'data': [],
				'fill': False,
				'borderColor': 'rgb(255, 204, 0)',
				'backgroundColor': 'rgb(255, 204, 0)',
				'tension': 0.1
			}

		timeout = {
				'label': 'Timeout',
				'data': [],
				'fill': False,
				'borderColor': 'rgb(102, 179, 255)',
				'backgroundColor': 'rgb(102, 179, 255)',
				'tension': 0.1
			}

		login = {
				'label': 'Logged in Logged out',
				'data': [],
				'fill': False,
				'borderColor': 'rgb(0, 153, 0)',
				'backgroundColor': 'rgb(0, 153, 0)',
				'tension': 0.1
			}


		for key, value in count_dict.items():
			login_count = 0
			timout_count = 0
			terminate_count = 0
			error_count = 0
			if value:
				for rec in value:
					if rec.state == 'logged_in' or rec.state == 'logged_out':
						login_count += 1
					elif rec.state == 'timed_out':
						timout_count += 1
					elif rec.state == 'terminated':
						terminate_count += 1
					elif rec.state == 'error':
						error_count += 1

			login['data'].append(login_count)
			timeout['data'].append(timout_count)
			terminate['data'].append(terminate_count)
			login_fail['data'].append(error_count)

		data['datasets'].append(login_fail)
		data['datasets'].append(terminate)
		data['datasets'].append(timeout)
		data['datasets'].append(login)


		_logger.info("===================>>>>>>>>>>>>>>>>>>data:%r",data)
		return {
		'data':data
		}



