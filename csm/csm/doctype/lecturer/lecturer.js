// Copyright (c) 2022, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Lecturer', {
	// refresh: function(frm) {

	// }
	user_id: function(frm) {
	    frappe.call({
            method: "csm.csm.utils.lecturer_existed",
            args: {
                "user_id": frm.doc.user_id
            },
            callback(res) {
                if (res.message) {
                    frm.set_value("user_id", "");
                    frappe.throw("Cán bộ giảng viên đã tồn tại.");
                } else {
                    frappe.call({
                    method: "csm.csm.utils.get_full_name",
                    args: {
                        "user_id": frm.doc.user_id
                    },
                    callback(res) {
                        frm.set_value('full_name', res.message);
                    }
                })
                }
            }
        })
	}
});
