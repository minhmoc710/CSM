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
			"fieldname": "subject_code",
			"label": "Môn học",
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
			"fieldname": "start_period",
			"label": "Tiết bắt đầu",
		},
		{
			"fieldname": "end_period",
			"label": "Tiết kết thúc",
		},
		{
			"fieldname": "day",
			"label": "Thứ",
		},
		{
			"fieldname": "room_id",
			"label": "Phòng",
			"fieldtype": "Link",
			"options": "Room"
		},
		{
			"fieldname": "semester",
			"label": "Kì học",
			"fieldtype": "Link",
			"options": "Semester"
		}
	]
	return columns, get_time_table_list(filters), get_message(filters)


def get_time_table_list(filters=None):
	if filters.semester:
		semester = f"AND smt.name = '{filters.semester}'"
	elif current_semester := get_current_semester():
		semester = f"AND smt.name = '{current_semester}'"
	else:
		semester = ""

	if filters.subject_code:
		subject = f" AND s.subject_code = '{filters.subject_code}' "
	else:
		subject = ""

	return frappe.db.sql(f"""
		SELECT tt.subject_class, tt.start_period, tt.end_period, tt.day, tt.room_id, s.subject_title, s.subject_code, sc.semester
		FROM `tabTime Table` tt
		JOIN `tabSubject Class` sc ON sc.name = tt.subject_class
		JOIN `tabClass Participant` cp ON cp.parent = sc.name
		JOIN `tabSubject` s ON s.name = sc.subject
		JOIN `tabSemester` smt ON smt.name = sc.semester
		WHERE
		    cp.participant = "nguyenvana@gmail.com" AND
		    cp.role = "Giảng viên"
		    {semester}
		    {subject}
		GROUP BY tt.subject_class
	""", as_dict=True)


def get_message(filters=None):
	semester = filters.semester or get_current_semester()

	user_full_name = frappe.db.get_value("User", frappe.session.user, "full_name")
	if semester:
		return f"Thời khóa biểu cho {user_full_name} trong học kì {semester}:"
	return f"Thời khóa biểu cho {user_full_name}:"
