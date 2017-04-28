odoo.define('hr_performance.hr_performance', function (require) {
"use strict";

var core = require('web.core');
var Model = require('web.DataModel');
var ListView = require('web.ListView');

var QWeb = core.qweb;
var _t = core._t;

var CompareListView = ListView.extend({
    render_buttons: function ($node) {
        if (!this.$buttons) {
            this.$buttons = $(QWeb.render("CompareListView.buttons", {'widget': this}));

            this.$buttons.find('.oe_generate_po').click(this.proxy('create_performancebonuscalculation'));

            $node = $node || this.options.$buttons;
            if ($node) {
                this.$buttons.appendTo($node);
            } else {
                this.$('.oe_list_buttons').replaceWith(this.$buttons);
            }
        }
    },

    create_performancebonuscalculation: function () {
        var self = this;
        new Model(self.dataset.model).call("create_performancebonuscalculation",[self.dataset.context.tender_id,self.dataset.context]).then(function(result) {
            self.ViewManager.action_manager.history_back();
        });
    },
});

core.view_registry.add('tree_performancebonuscalculation', CompareListView);

});