// Copyright (c) 2022, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Subject', {
	// refresh: function(frm) {

	// }
	credit_num: function(frm) {
        if (frm.doc.credit_num < 0) {
            frm.set_value("credit_num", 1);
            frappe.throw("Số tín chỉ phải lớn hơn 0.");
        }
	}

});
