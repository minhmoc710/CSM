// Copyright (c) 2022, Minh and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Đề tài nghiên cứu khoa học"] = {
	"filters": [
        {
			"fieldname": "from",
			"label": "Thời gian bắt đầu",
			"fieldtype": "Date",
		},
		{
			"fieldname": "to",
			"label": "Thời gian kết thúc",
			"fieldtype": "Date"
		},
	],
	onload: function(report) {
	    report.page.add_inner_button(("Xóa bộ lọc"), function() {
			console.log(report);
			report.set_filter_value('from', []);
			report.set_filter_value('to', []);
			report.refresh();
		});
	}
};
