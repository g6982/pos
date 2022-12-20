# -*- coding: utf-8 -*-
{
  "name": "Odoo User Login Security",
  "summary": """Secure your Odoo from Intruders with User Login Security""",
  "category": "Extra Tools",
  "version": "1.0.3",
  "sequence": 1,
  "author": "Webkul Software Pvt. Ltd.",
  "license": "Other proprietary",
  "website": "https://store.webkul.com/Odoo-User-Login-Security.html",
  "description": """""",
  "depends": ['auth_signup','web','portal'],
  "data":[
		'security/security.xml',
		'security/ir.model.access.csv',
		'views/dashboard.xml',
		'views/res_users.xml',
		'views/session.xml',
		'views/res_config_settings.xml',
		'views/security_question_answer.xml',
		'views/security_question.xml',
		# 'templates/web.xml',
		'templates/mail.xml',
		'data/ir_actions_server.xml',
		'data/ir_cron.xml',
		'data/ir_config_parameter.xml',
		'wizard/update_question_answer.xml',
  ],
  "qweb":[
    'static/src/xml/dashboard.xml',
    'static/src/xml/update_que_ans.xml',
  ],
  'assets': {
    'web.assets_frontend': [
      'odoo_user_login_security/static/src/js/login.js',
      'odoo_user_login_security/static/src/js/password.js',
    ],
    'web.assets_backend': [
      'odoo_user_login_security/static/src/css/dashboard.css',
      'odoo_user_login_security/static/src/css/owl.carousel.min.css',
      'odoo_user_login_security/static/src/css/owl.theme.default.min.css',
      'odoo_user_login_security/static/src/js/dashboard.js',
      'odoo_user_login_security/static/src/js/jquery.mousewheel.min.js',
      'odoo_user_login_security/static/src/js/owl.carousel.min.js',
      'odoo_user_login_security/static/src/js/update_que_ans.js',
    ],
    'web.assets_qweb': [
      'user_login_security/static/src/xml/**/*',
    ]
  },

  "demo":[
    'demo/security.xml',
    'demo/session.session.csv',
  ],
  "images": ['static/description/banner.png'],
  "application": True,
  "price": 99,
  "currency": "USD",
}
