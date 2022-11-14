# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from csm.csm.utils import get_current_semester


def execute(filters=None):
	columns = [
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

	return frappe.db.sql(f"""
		SELECT er.room_id, e.subject_class, sc.subject, er.start_time, er.end_time, s.subject_title
		FROM `tabExam Room` er
		JOIN `tabExam Invigilator` ei ON ei.parent = er.name
		JOIN `tabExam` e ON e.name = er.exam
		JOIN `tabSubject Class` sc ON e.subject_class = sc.name
		JOIN `tabSubject` s ON s.name = sc.subject
		WHERE ei.invigilator = "nguyenvana@gmail.com" {semester}
	""", as_dict=True)
