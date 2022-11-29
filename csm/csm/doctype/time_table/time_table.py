# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from csm.csm.api import set_user_permission_for_doc


class TimeTable(Document):
	def on_update(self):
		subject_class_lecturer_id = [item['user_id'] for item in frappe.db.sql(f"""
			SELECT l.user_id
			FROM `tabTime Table` tt
			JOIN `tabSubject Class` sc ON sc.name = tt.subject_class
			JOIN `tabLecturer` l ON l.name = sc.lecturer
			WHERE tt.name = "{self.name}"
		""")]
		set_user_permission_for_doc(subject_class_lecturer_id, "Time Table", self.name)
