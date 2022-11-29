# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from csm.csm.utils import get_current_semester


def execute(filters=None):
	columns = [
		{
			"fieldname": "title",
			"label": "Chủ đề",
			"width": 400,
			"fieldtype": "Link",
			"options": "Thesis"
		},
		{
			"fieldname": "student",
			"label": "Sinh viên"
		},
		{
			"fieldname": "major",
			"label": "Khoa",
			"fieldtype": "Link",
			"options": "Major"
		},
		{
			"fieldname": "specialization",
			"label": "Ngành",
			"fieldtype": "Link",
			"options": "Specialization"
		},
		{
			"fieldname": "defense_time",
			"label": "Thời gian bảo vệ",
		},
		{
			"fieldname": "committee",
			"label": "Hội đồng chấm",
			"fieldtype": "Link",
			"options": "Thesis Committee"
		},
		{
			"fieldname": "main_critic",
			"label": "Người phản biện chính",
			"fieldtype": "Link",
			"options": "User"
		}
	]
	return columns, get_thesis_list(filters)


def get_thesis_list(filters=None):
	if filters.semester:
		semester = f"AND t.semester = '{filters.semester}'"
	elif current_semester := get_current_semester():
		semester = f"AND t.semester = '{current_semester}'"
	else:
		semester = ""

	if "System Manager" in frappe.get_roles():
		user_filter = ""
	else:
		user_filter = f" AND tcm.member = '{frappe.session.user}'"

	return frappe.db.sql(f"""
		SELECT DISTINCT t.title, t.major, t.committee, t.specialization, t.defense_time, t.student
		FROM `tabThesis` t
		JOIN `tabThesis Committee` tc ON t.committee = tc.name
		JOIN `tabThesis Committee Member` tcm ON tcm.parent = tc.name
		WHERE  
			is_finished != 1
			{user_filter}
			{semester}
	""", as_dict=True)
