# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from csm.csm.utils import get_current_semester

def execute(filters=None):
	columns = [
		{
			"fieldname": "name",
			"label": "Đề tài",
			"fieldtype": "Link",
			"options": "Scientific Research Subject"
		},
		{
			"fieldname": "start_time",
			"label": "Thời gian bắt đầu"
		},
		{
			"fieldname": "end_time",
			"label": "Thời gian kết thúc",
		}
	]
	return columns, get_research_subject_data(filters), "Danh sách Đề tài NCKH"


def get_research_subject_data(filters):
	if None not in (filters.get('from'), filters.get('to')):
		from_time = filters.get('from')
		to_time = filters.get('to')
		from_to = f" AND srs.creation BETWEEN '{from_time}' AND '{to_time}' "
	elif filters.get('from') is None and filters.get('to') is not None:
		to_time = filters.get('to')
		from_to = f" AND srs.creation BETWEEN '1970-01-01' AND '{to_time}' "
	elif filters.get('from') is not None and filters.get('to') is None:
		from_time = filters.get('from')
		from_to = f" AND srs.creation BETWEEN '{from_time}' AND '{frappe.utils.nowdate()}' "
	else:
		from_to = ""

	return frappe.db.sql(f"""
		SELECT srs.name, srs.start_time, srs.end_time
		FROM `tabScientific Research Subject` srs
		JOIN `tabContributor` c ON c.parent = srs.name
		WHERE
		    c.participant = "nguyenvana@gmail.com"
		    {from_to}
		ORDER BY srs.creation DESC
	""", as_dict=True)