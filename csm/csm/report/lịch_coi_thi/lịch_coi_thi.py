# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from csm.csm.utils import get_current_semester


def execute(filters=None):
	columns = [
		{
			"fieldname": "name",
			"label": "Ca coi thi",
			"fieldtype": "Link",
			"options": "Exam Shift"
		},
		{
			"fieldname": "subject_title",
			"label": "Tên môn học",
		},
		{
			"fieldname": "subject",
			"label": "Mã môn học",
			"fieldtype": "Link",
			"options": "Subject"
		},
		{
			"fieldname": "subject_class",
			"label": "Lớp",
			"fieldtype": "Link",
			"options": "Subject Class"
		},
		{
			"fieldname": "room_id",
			"label": "Phòng thi",
			"fieldtype": "Link",
			"options": "Room"
		},
		{
			"fieldname": "start_time",
			"label": "Thời gian bắt đầu",
		},
		{
			"fieldname": "end_time",
			"label": "Thời gian kết thúc",
		}
	]
	return columns, get_exams(filters)


def get_exams(filters):
	if filters.semester:
		semester = f"AND semester_id = '{filters.semester}'"
	elif current_semester := get_current_semester():
		semester = f"AND semester_id = '{current_semester}'"
	else:
		semester = ""

	if "System Manager" in frappe.get_roles():
		user_filter = "1 = 1"
	else:
		user_filter = f" ei.invigilator = '{frappe.session.user}'"

	return frappe.db.sql(f"""
		SELECT 
			er.name, er.room_id, e.subject_class, sc.subject, er.start_time, er.end_time, s.subject_title
		FROM `tabExam Shift` er
		JOIN `tabExam Invigilator` ei ON ei.parent = er.name
		JOIN `tabExam` e ON e.name = er.exam
		JOIN `tabSubject Class` sc ON e.subject_class = sc.name
		JOIN `tabSubject` s ON s.name = sc.subject
		WHERE
			{user_filter}
			{semester}
		GROUP BY er.room_id
	""", as_dict=True)
