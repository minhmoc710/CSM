# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document
from csm.csm.api import set_user_permission_for_doc
from frappe import db


class Thesis(Document):
	def on_update(self):
		advisor_user_id = db.get_value("Lecturer", self.advisor, "user_id")
		set_user_permission_for_doc([advisor_user_id, self.student], "Thesis", self.name)
