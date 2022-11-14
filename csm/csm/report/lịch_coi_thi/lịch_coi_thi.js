// Copyright (c) 2022, Frappe Technologies and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Lịch coi thi"] = {
	"filters": [
        {
			"fieldname": "semester",
			"label": "Kì học",
			"fieldtype": "Link",
			"options": "Semester"
		},
	]
};
