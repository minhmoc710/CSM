# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from csm.csm.api import set_user_permission_for_doc


class SubjectClass(Document):
	def on_update(self):
		# Add permission for every lecturer of the class
		lecturer_user_id = frappe.db.get_value("Lecturer", self.lecturer, "user_id")
		set_user_permission_for_doc([lecturer_user_id], "Subject Class", self.name)

		# Add permission for every lecturer to the class's exams
		exam_ids = [item['exam_id'] for item in frappe.db.sql(f"""
			SELECT name exam_id
			FROM `tabExam` e
			WHERE e.subject_class = "{self.name}"
		""")]
		for exam_id in exam_ids:
			set_user_permission_for_doc([lecturer_user_id], "Exam", exam_id)

		# Add permission for every lecturer to the time table
		time_table_ids = [item['name'] for item in frappe.db.sql(f"""
			SELECT tt.name 
			FROM `tabTime Table` tt
			WHERE tt.subject_class = "{self.name}"
		""")]
		for time_table_id in time_table_ids:
			set_user_permission_for_doc([lecturer_user_id], "Time Table", time_table_id)
