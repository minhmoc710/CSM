# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from csm.csm.api import set_user_permission_for_doc


class ExamShift(Document):
	def on_update(self):
		invigilator_user_ids = [item['user_id'] for item in frappe.db.sql(f"""
			SELECT ei.invigilator user_id
			FROM `tabExam Shift` es
			JOIN `tabExam Invigilator` ei ON ei.parent = es.name
			WHERE es.name = "{self.name}"
		""", as_dict=True)]
		set_user_permission_for_doc(invigilator_user_ids, "Exam Shift", self.name)
