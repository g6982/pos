odoo.define('pos_show_dual_currency.OrderWidget', function(require) {
    'use strict';

    const { useState, useRef, onPatched } = owl.hooks;
    const { Component } = owl;

    const OrderWidget = require('point_of_sale.OrderWidget');
    const Registries = require('point_of_sale.Registries');

    const PosShowDualCurrencyOrderWidget = (OrderWidget) =>
        class extends OrderWidget {
            constructor() {
                super(...arguments);
                this.state = useState({ total: 0, tax: 0, currencyTotal:0, currencyTax:0 });

            }

            _updateSummary() {
               // console.log('_updateSummary');
                
                if (!this.order.get_orderlines().length) {
                    return;
                }
                const current = Component.current;

                const total = this.order ? this.order.get_total_with_tax() : 0;
                const taxes = this.order ? total - this.order.get_total_without_tax() : 0;
                if(this.env.pos.config.show_dual_currency){
                    var tasa_usd = this.env.pos.config.show_currency_rate_real;
                    var text_usd = "USD : " + tasa_usd.toFixed(2) ;
                    $('.currency_dollar').text(text_usd);
                    var tasa_eur = this.env.pos.config.show_currency_rate_real_euro;
                    var text_eur = " EUR : " + tasa_eur.toFixed(2) ;;
                    $('.currency_euro').text(text_eur);

                    var total_currency = 0;
                    var taxes_currency = 0;
                    var rate_company = parseFloat(this.env.pos.config.rate_company);
                    var show_currency_rate = parseFloat(this.env.pos.config.show_currency_rate);
                    var show_currency_rate_real = parseFloat(this.env.pos.config.show_currency_rate_real)
                    
                    if(rate_company > show_currency_rate){
                        total_currency = total / show_currency_rate_real;
                        taxes_currency = taxes / show_currency_rate_real;
                    }
                    else if(rate_company < show_currency_rate){
                        if(show_currency_rate>0){
                            total_currency = total * show_currency_rate_real;
                            taxes_currency = taxes * show_currency_rate_real;
                        }
                    }
                    else{
                        total_currency = total;
                        taxes_currency = taxes;
                    }
    
                    this.state.currencyTotal = this.env.pos.format_currency_no_symbol(total_currency);
                    this.state.currencyTax = this.env.pos.format_currency_no_symbol(taxes_currency);
                    
                    /* aqui se debe renderizar los campos currencyTotal y currencyTax en la vista */
                  //  console.log('=>>', $('.currencyTotal'));
                    
                    $('.currencyTotal').text(this.env.pos.format_currency_no_symbol(total_currency));
                    $('.currencyTax').text(this.env.pos.format_currency_no_symbol(taxes_currency));
                }
                
                super._updateSummary()
            }
        };

    Registries.Component.extend(OrderWidget, PosShowDualCurrencyOrderWidget);

    return OrderWidget;
});
