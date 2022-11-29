# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from csm.csm.exam_api import create_default_lists_for_exam
from csm.csm.api import set_user_permission_for_doc


class Exam(Document):
	def on_update(self):
		class_lecturer = frappe.db.sql(f"""
			SELECT l.user_id
			FROM `tabExam` e
			JOIN `tabSubject Class` sc ON sc.name = e.subject_class
			JOIN `tabLecturer` l ON l.name = sc.lecturer
		""", as_dict=True)
		if class_lecturer:
			class_lecturer_user_id = class_lecturer[0]['user_id']
			set_user_permission_for_doc([class_lecturer_user_id], "Exam", self.name)

	def after_insert(self):
		create_default_lists_for_exam(self.name)
