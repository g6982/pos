odoo.define('pos_show_dual_currency.ProductScreen', function (require) {
    'use strict';

    const NumberBuffer = require('point_of_sale.NumberBuffer');
    const Registries = require('point_of_sale.Registries');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const PosShowDualCurrencyProductScreen = (ProductScreen) =>
        class extends ProductScreen {
            constructor() {
                super(...arguments);
            }
            _onClickPay() {
                const order = this.currentOrder;
                if (order.orderlines.models.length < 9){
                    super._onClickPay()
                }else{
                    alert("No puede tener mas de 8 Item")
                }
            }
        };

    Registries.Component.extend(ProductScreen, PosShowDualCurrencyProductScreen);

    return ProductScreen;
});
