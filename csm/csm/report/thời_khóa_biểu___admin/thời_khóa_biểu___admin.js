// Copyright (c) 2022, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Thời khóa biểu"] = {
	"filters": [
        {
			"fieldname": "semester",
			"label": "Kì học",
			"fieldtype": "Link",
			"options": "Semester"
		},
		{
			"fieldname": "subject_code",
			"label": "Môn học",
			"fieldtype": "Link",
			"options": "Subject"
		},
	]
};
