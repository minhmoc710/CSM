// Copyright (c) 2022, Minh and contributors
// For license information, please see license.txt

frappe.ui.form.on('Exam Ban List', {
	// refresh: function(frm) {

	// }
	after_save: function(frm){
	    frappe.call({
	        method: "csm.csm.exam_api.remove_exempted_students_from_ban_list",
	        args: {
	            exam_id: frm.doc.exam
	        },
	        callback(res) {
	            if (res.message.length > 0) {
                    frappe.msgprint({
                        title: "Lỗi",
                        message: `Không thể thêm các sinh viên: ${res.message} vì họ đã tồn tại trong danh sách miễn thi`,
                        primary_action: {
                            label: "OK",
                            action(values) {
                                window.location.reload();
                            }
                        }
                    })
                    frappe.throw();

	            }
	        }
	    })
	}
});

frappe.ui.form.on("Students List", {
    banned_students_add(frm, cdt, cdn) {
        let inserted_students = frm.doc.banned_students.map(item => item.student);
        inserted_students = inserted_students.filter(item => item)

        frappe.call({
            method: "csm.csm.exam_api.check_students_in_exempt_list",
            args: {
                "student_ids": inserted_students,
                "exam_id": frm.doc.exam
            },
            callback(res) {
                if (res.message.length > 0) {
                    frappe.throw(`Không thể thêm các sinh viên: ${res.message} vì họ đã tồn tại trong danh sách miễn thi`);
                };
            }
        })
    }
})
