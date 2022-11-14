// Copyright (c) 2022, Frappe Technologies and contributors
// For license information, please see license.txt

frappe.ui.form.on('Time Table', {
    subject_class : function(frm) {
        frappe.call({
                method: "csm.csm.utils.get_subject_class_credit_num",
                args: {
                    "subject_class_id": frm.doc.subject_class
                },
                callback(res) {
                    frm.set_value("end_period",Number(frm.doc.start_period) + Number(res.message) - 1)
                }
            })
    },
	start_period: function(frm) {
	    let subject_id = frm.doc.subject_class;
	    if (subject_id) {
	        frappe.call({
                method: "csm.csm.utils.get_subject_class_credit_num",
                args: {
                    "subject_class_id": subject_id
                },
                callback(res) {
                    frm.set_value("end_period",Number(frm.doc.start_period) + Number(res.message) - 1)
                }
            })
	    } else {
	        frm.set_value("end_period", frm.doc.start_period);
	    }
	},
	end_period: function(frm) {
	    if (Number(frm.doc.end_period) < Number(frm.doc.start_period)){
	        frm.set_value("end_period", frm.doc.start_period);
	        frappe.throw("Tiết kết thúc phải lớn hơn hoặc bằng tiết bắt đầu.")
	    }
	}
});
