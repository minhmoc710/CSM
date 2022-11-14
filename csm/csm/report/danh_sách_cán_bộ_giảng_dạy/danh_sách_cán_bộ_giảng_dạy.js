// Copyright (c) 2022, Minh and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Danh sách cán bộ giảng dạy"] = {
	"filters": [
        {
			"fieldname": "from",
			"label": "Tham gia từ ngày",
			"fieldtype": "Date",
		},
		{
			"fieldname": "to",
			"label": "Đến ngày",
			"fieldtype": "Date"
		},
		{
		    "fieldname": "degree",
		    "label": "Học vị",
		    "fieldtype": "Select",
		    "options": "Không\nCử nhân\nThạc sĩ\nTiến sĩ"
		},
		{
		    "fieldname": "academic_rank",
		    "label": "Học hàm",
		    "fieldtype": "Select",
		    "options": "Không\nPhó giáo sư\nGiáo sư"
		},
		{
		    "fieldname": "remove_filters",
		    "label": "Xóa bộ lọc",
		    "fieldtype": "Button",
		    onchange: (query_report) => { console.log('please work!'); frappe.msgprint("test")}
		}
	],
	onload: function(report) {
	    report.page.add_inner_button(("Xóa bộ lọc"), function() {
			console.log(report);
			report.set_filter_value('academic_rank', []),
			report.set_filter_value('degree', []),
			report.refresh();
		});

	}
};
