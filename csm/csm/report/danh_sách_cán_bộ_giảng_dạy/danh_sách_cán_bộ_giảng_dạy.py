# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from csm.csm.utils import get_current_semester

def execute(filters=None):
	columns = [
		{
			"fieldname": "name",
			"label": "ID",
			"fieldtype": "Link",
			"options": "Lecturer"
		},
		{
			"fieldname": "full_name",
			"label": "Họ và tên"
		},
		{
			"fieldname": "join_date",
			"label": "Ngày tham gia",
			"fieldtype": "Date",
		},
		{
			"fieldname": "highest_degree",
			"label": "Học hàm",
		},
		{
			"fieldname": "highest_academic_rank",
			"label": "Học vị",
		},
		{
			"fieldname": "total_publications",
			"label": "Số sản nghiên cứu/bài báo/sách",
		},
		{
			"fieldname": "total_products",
			"label": "Số sản phẩm khoa học",
			"fieldtype": "Int"
		}
	]
	return columns, get_time_table_list(filters), get_message(filters)


def get_highest_academic_rank(lecturer_id):
	academic_rank_levels = {
		"Không": 0,
		"Giáo sư": 1,
		"Phó giáo sư": 2
	}
	highest_academic_rank = 0
	highest_rank_title = "Không"

	academic_history_data = frappe.db.sql(f"""
		SELECT academic_rank
		FROM `tabAcademic History`
		WHERE parent = "{lecturer_id}"
	""", as_dict=True)

	for academic_record in academic_history_data:
		if academic_rank_levels[academic_record['academic_rank']] > highest_academic_rank:
			highest_academic_rank = academic_rank_levels[academic_record['academic_rank']]
			highest_rank_title = academic_record['academic_rank']
	return highest_rank_title


def get_highest_degree(lecturer_id):
	degree_levels = {
		"Không": -1,
		"Cử nhân": 0,
		"Thạc sĩ": 1,
		"Tiến sĩ": 2,
		"Tiến sĩ khoa học": 3
	}
	highest_degree_level = -1
	highest_degree_title = "Không"

	academic_history_data = frappe.db.sql(f"""
		SELECT degree
		FROM `tabAcademic History`
		WHERE parent = "{lecturer_id}"
	""", as_dict=True)

	for academic_record in academic_history_data:
		if degree_levels[academic_record['degree']] > highest_degree_level:
			highest_degree_level = degree_levels[academic_record['degree']]
			highest_degree_title = academic_record['degree']
	return highest_degree_title


def get_number_of_publications(lecturer_id):
	number_of_publications_data = frappe.db.sql(f"""
		SELECT COUNT(*) count
		FROM `tabUser Scientific Publications`
		WHERE parent = "{lecturer_id}"
	""", as_dict=True)
	if number_of_publications_data:
		return number_of_publications_data[0]['count']
	else:
		return 0


def get_number_of_scientific_products(lecturer_id):
	number_of_publications_data = frappe.db.sql(f"""
		SELECT COUNT(*) count
		FROM `tabUser Scientific Products`
		WHERE parent = "{lecturer_id}"
	""", as_dict=True)
	if number_of_publications_data:
		return number_of_publications_data[0]['count']
	else:
		return 0


def get_time_table_list(filters=None):
	if None not in (filters.get('from'), filters.get('to')):
		from_time = filters.get('from')
		to_time = filters.get('to')
		from_to = f" AND l.creation BETWEEN '{from_time}' AND '{to_time}' "
	elif filters.get('from') is None and filters.get('to') is not None:
		to_time = filters.get('to')
		from_to = f" AND l.creation BETWEEN '1970-01-01' AND '{to_time}' "
	elif filters.get('from') is not None and filters.get('to') is None:
		from_time = filters.get('from')
		from_to = f" AND l.creation BETWEEN '{from_time}' AND '{frappe.utils.nowdate()}' "
	else:
		from_to = ""

	lecturer_list = frappe.db.sql(f"""
		SELECT l.name, l.full_name, l.join_date
		FROM `tabLecturer` l
		JOIN `tabUser Scientific Publications` usp ON usp.parent = l.name
		JOIN `tabUser` u ON l.user_id = u.name
		WHERE
			1 = 1
			{from_to}
		ORDER BY u.first_name, u.last_name
	""", as_dict=True)

	result = []
	for lecturer in lecturer_list:
		lecturer['highest_academic_rank'] = get_highest_academic_rank(lecturer['name'])
		if filters.get('academic_rank') is not None:
			if filters.get('academic_rank') != lecturer['highest_academic_rank']:
				continue
		lecturer['highest_degree'] = get_highest_degree(lecturer['name'])
		if filters.get('degree') is not None:
			if filters.get('degree') != lecturer['highest_degree']:
				continue
		lecturer['total_publications'] = get_number_of_publications(lecturer['name'])
		lecturer['total_products'] = get_number_of_scientific_products(lecturer['name'])

		result.append(lecturer)
	return result


def get_message(filters=None):
	semester = filters.semester or get_current_semester()

	user_full_name = frappe.db.get_value("User", frappe.session.user, "full_name")
	if semester:
		return f"Thời khóa biểu cho {user_full_name} trong học kì {semester}:"
	return f"Thời khóa biểu cho {user_full_name}:"
