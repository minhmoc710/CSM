# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from csm.csm.utils import get_current_semester


def execute(filters=None):
	columns = [
		{
			"fieldname": "name",
			"label": "Tên",
			"fieldtype": "Link",
			"options": "Subject Class"
		},
		{
			"fieldname": "class_name",
			"label": "Lớp"
		},
		{
			"fieldname": "class_code",
			"label": "Mã lớp"
		},
		{
			"fieldname": "subject",
			"label": "Mã môn học",
			"fieldtype": "Link",
			"options": "Subject"
		},
		{
			"fieldname": "subject_title",
			"label": "Tên môn học",
			"width": 300,
		},
		{
			"fieldname": "credit_num",
			"label": "Số tín chỉ"
		},
		{
			"fieldname": "start_date",
			"label": "Ngày bắt đầu"
		},
		{
			"fieldname": "end_date",
			"label": "Ngày kết thúc"
		}
	]
	return columns, get_class_list(filters)


def get_class_list(filters=None):
	if filters.semester:
		semester = f"AND smt.name = '{filters.semester}'"
	elif current_semester := get_current_semester():
		semester = f"AND smt.name = '{current_semester}'"
	else:
		semester = ""

	if "System Manager" in frappe.get_roles():
		user_filter = "1 = 1"
	else:
		user_filter = f"l.user_id = '{frappe.session.user}'"

	return frappe.db.sql(f"""
		SELECT
			sc.name, sc.class_name, sc.class_code, sc.subject, sc.start_date, sc.end_date,
			s.subject_title, s.credit_num
		FROM `tabSubject Class` sc
		JOIN `tabLecturer` l ON sc.lecturer = l.name 
		JOIN `tabSubject` s ON sc.subject = s.name
		JOIN `tabSemester` smt ON smt.name = sc.semester
		WHERE
			{user_filter}
		    {semester}
	""", as_dict=True)
