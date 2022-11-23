// Copyright (c) 2022, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Danh sách lớp"] = {
	"filters": [
        {
			"fieldname": "semester",
			"label": "Kì học",
			"fieldtype": "Link",
			"options": "Semester"
		},
	],
	onload: function(report) {
	    report.page.add_inner_button(("Xóa bộ lọc"), function() {
			console.log(report);
			report.set_filter_value('semester', []);
			report.refresh();
		});
	}
};
