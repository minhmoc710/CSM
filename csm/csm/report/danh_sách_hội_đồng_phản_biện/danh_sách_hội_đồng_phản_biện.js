// Copyright (c) 2022, Minh and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Danh sách hội đồng phản biện"] = {
    "filters": [
        {
			"fieldname": "semester",
			"label": "Kì học",
			"fieldtype": "Link",
			"options": "Semester"
		},
	]
};
