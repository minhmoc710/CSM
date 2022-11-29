# Copyright (c) 2022, Frappe Technologies and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from csm.csm.api import set_user_permission_for_doc
from frappe import db


class Thesis(Document):
	def on_update(self):

		advisor_user_id = db.get_value("Lecturer", self.advisor, "user_id")

		thesis_critics_user_ids = [item['user_id'] for item in frappe.db.sql(f"""
			SELECT l.user_id
			FROM `tabThesis Critics` tc 
			JOIN `tabLecturer` l ON tc.critic = l.name
			WHERE tc.parent = "{self.name}"
		""", as_dict=True)]

		thesis_committee_members_user_ids = [item['member'] for item in frappe.db.sql(f"""
			SELECT tcm.member
			FROM `tabThesis Committee Member` tcm 
			JOIN `tabThesis Committee` tc ON tc.name = tcm.parent
			WHERE tc.name = "{self.committee}"
		""", as_dict=True)]

		user_ids = set([advisor_user_id] + thesis_critics_user_ids + thesis_committee_members_user_ids)

		set_user_permission_for_doc(user_ids, "Thesis", self.name)
