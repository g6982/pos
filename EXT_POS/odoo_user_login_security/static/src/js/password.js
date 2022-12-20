odoo.define('odoo_user_login_security.password',function (require) {
	'use strict';

  	var core = require('web.core');
    var ajax = require('web.ajax');
    var signup = require('auth_signup.signup');
    var publicWidget = require('web.public.widget');

    var _t = core._t;
    console.log("inside password js file")
	console.log("again checking it")
	var signup_pass = $('.oe_signup_form').find('input[name="enable_password_security"]').val();
	var reset_pass = $('.oe_reset_password_form').find('input[name="enable_password_security"]').val();
	var msg = "Password Must Contain:\n\t*Atleast 1 lower latter\n\t*Atleast 1 Upper latter\n\t*Atleast 1 Number\n\t*Atleast 1 Special Charector\n\t*Minimum 8 Charector."
	console.log("signup_pass:",signup_pass)
	console.log("reset_pass:",reset_pass)
	$(document).on('change','.questions',function(e){
		var val = $(this).val();
		$('.questions').find('option').show();
		console.log("val:",val)
		var notSelected = $(".questions option:selected");
		var array = notSelected.map(function () {
			return this.value;
		}).get();
		console.log("selected:",array)
		if(array.length > 0){
			$.each(array, function( index, value ) {
				console.log("index:",index,"value:",value );
				$(`.questions option[value="${value}"]`).not(this).hide();
			  });
		}
	})

	publicWidget.registry.SignUpForm = publicWidget.Widget.extend({
		selector: '.oe_signup_form',
		events: {
			'submit': '_onSubmit',
		},
		_onSubmit: function (e) {
			var self = this;
			var val = $('#password').val();
			console.log("inside submit password")
			if(signup_pass || reset_pass){
				check_password_strength(self,e,val)
			}
		},
	});
	publicWidget.registry.resetpassword = publicWidget.Widget.extend({
		selector: '.oe_reset_password_form',
		events: {
			'submit': '_onSubmit',
		},

		_onSubmit: function (e) {
			var self = this;
			console.log("inside reset password")
			var token = $('.oe_reset_password_form').find('input[name="token"]').val();
			if(token){
				console.log("inside reset password")
				var val = $('#password').val();
				if(signup_pass || reset_pass){
					check_password_strength(self,e,val)
				}

			}

		},
	});


    function check_password_strength(self,e,password) {
        var pattern = /^(?=.*[0-9])(?=.*[!@#*])(?=.*[a-z])(?=.*[A-Z]).{8,}$/g;
		console.log("check password:",password)
        if(password.match(pattern)){
            var $btn = self.$('.oe_login_buttons > button[type="submit"]');
            $btn.attr('disabled', 'disabled');
            $btn.prepend('<i class="fa fa-refresh fa-spin"/> ');
        }
        else {
            alert(msg)
            e.preventDefault()
        }
    }

});
