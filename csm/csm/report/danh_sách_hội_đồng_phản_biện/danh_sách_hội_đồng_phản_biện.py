# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from csm.csm.utils import get_current_semester

def execute(filters=None):
	columns = [
		{
			"fieldname": "committee_name",
			"label": "Hội đồng",
			"fieldtype": "Link",
			"options": "Thesis Committee"
		},
		{
			"fieldname": "semester_id",
			"label": "Kì học",
			"fieldtype": "Link",
			"options": "Semester"
		},
		{
			"fieldname": "member_count",
			"label": "Số lượng thành viên",
			"fieldtype": "Int",
		}
	]
	return columns, get_research_subject_data(filters), "Danh sách Hội đồng phản biện"


def get_research_subject_data(filters):
	if filters.semester:
		semester = f"semester_id = '{filters.semester}'"
	elif current_semester := get_current_semester():
		semester = f"semester_id = '{current_semester}'"
	else:
		semester = ""
	return frappe.db.sql(f"""
		SELECT committee_name, semester_id, COUNT(tcm.name) member_count
		FROM `tabThesis Committee` tc
		JOIN `tabThesis Committee Member` tcm ON tcm.parent = tc.name
		WHERE
			{semester}
		GROUP BY committee_name
		ORDER BY committee_name
	""", as_dict=True)