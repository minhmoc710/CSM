import frappe
from frappe import db
from datetime import datetime


@frappe.whitelist()
def get_current_semester() -> str:
    current_time = datetime.now()
    current_time_str = current_time.strftime("%Y-%m-%d")
    semesters_data = db.sql(f"""
        SELECT name
        FROM `tabSemester`
        WHERE
            "{current_time_str}" BETWEEN start_date AND end_date
        ORDER BY end_date DESC
        LIMIT 1
    """, as_dict=True)
    return "" if not semesters_data else semesters_data[0]['name']


@frappe.whitelist()
def get_full_name(user_id) -> str:
    return frappe.db.get_value("User", user_id, "full_name")


@frappe.whitelist()
def lecturer_existed(user_id) -> bool:
    return frappe.db.exists("Lecturer", {"user_id": user_id})


@frappe.whitelist()
def get_subject_class_credit_num(subject_class_id):
    data = db.sql(f"""
        SELECT credit_num
        FROM `tabSubject` s
        JOIN `tabSubject Class` sc ON s.name = sc.subject
        WHERE sc.name = "{subject_class_id}"
    """, as_dict=True)
    if data:
        return data[0]['credit_num']
    else:
        return 0