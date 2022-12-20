odoo.define('odoo_user_login_security.update_que_ans', function (require) {
	"use strict";

	/**
	 * This file defines a client action that opens in a dialog (target='new') and
	 * allows the user to update his security question and answer.
	 */

	var AbstractAction = require('web.AbstractAction');
	var core = require('web.core');
	var Dialog = require('web.Dialog');
	var web_client = require('web.web_client');

	var _t = core._t;

	var UpdateQuestionAnswer = AbstractAction.extend({
		template: "UpdateQuestionAnswer",


		init: function (parent, action, options) {
			var self = this;
			this._super.apply(this, arguments);

			this.action = action;
			this.context = action.context;
			this.options = options || {};
			console.log("init:",this.action.params)
			self.params = this.action.params
			console.log()
			self.num_of_que = this.action.params.num_of_que
			self.questions = this.action.params.questions
			self.enable = this.action.params.enable
			console.log(typeof self.num_of_que)
			console.log(typeof self.enable)


		},



		start: function () {
			var self = this;
			web_client.set_title(_t("Update Security Question Answer"));
			var $button = self.$('.oe_form_button');
			$button.appendTo(this.getParent().$footer);
			$button.eq(1).click(function () {
				self.$el.parents('.modal').modal('hide');
			});
			$button.eq(0).click(function () {

				self._rpc({
						route: '/web/update_que_ans',
						params: {
							fields: $('form[name=update_que_ans_form]').serializeArray()
						}
					})
				self.$el.parents('.modal').modal('hide');
			});
		},

	});

	core.action_registry.add("update_que_ans", UpdateQuestionAnswer);

	return UpdateQuestionAnswer;

	});
