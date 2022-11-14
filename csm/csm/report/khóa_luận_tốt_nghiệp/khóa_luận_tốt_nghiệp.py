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
			"fieldname": "full_name",
			"label": "Sinh viên"
		},
		{
			"fieldname": "major",
			"label": "Ngành",
			"fieldtype": "Link",
			"options": "Major"
		},
		{
			"fieldname": "specialization",
			"label": "Chuyên ngành",
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

	return frappe.db.sql(f"""
		SELECT t.title, t.major, t.committee, t.specialization, t.defense_time, u.full_name, t.main_critic
		FROM `tabThesis` t
		JOIN `tabUser` u ON u.name = t.student
		WHERE 
			advisor = "nguyenvana@gmail.com" AND 
			is_finished != 1
			{semester}
	""", as_dict=True)
