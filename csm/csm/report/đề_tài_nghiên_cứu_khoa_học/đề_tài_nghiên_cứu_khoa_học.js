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
	]
};
