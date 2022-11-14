// Copyright (c) 2022, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Thesis Committee', {
	// refresh: function(frm) {

	// }
	setup: function(frm) {
	    frappe.call({
            method: "csm.csm.utils.get_current_semester",
            args: {},
            callback(res) {
                frm.set_value('semester_id', res.message);
            }
        })
	}
});
