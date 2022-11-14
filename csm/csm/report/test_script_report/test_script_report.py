# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = [
		{
			"fieldname": "name",
			"label": "Tên",
			"fieldtype": "Link",
			"options": "Subject Class",
			"width": 300
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
			"label": "Môn học",
			"fieldtype": "Link",
			"options": "Subject",
			"width": 300
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
	print(get_time_table_list())
	return columns, get_time_table_list()


def get_time_table_list():
	return frappe.db.sql(f"""
		SELECT sc.name, sc.class_name, sc.class_code, sc.subject, sc.start_date, sc.end_date
		FROM `tabSubject Class` sc
		JOIN `tabClass Participant` cp ON cp.parent = sc.name
		WHERE
		    participant = "nguyenvana@vnu.edu.vn" AND
# 		    participant = "{frappe.session.user}" AND
		    role = "Giảng viên"
	""", as_dict=True)
