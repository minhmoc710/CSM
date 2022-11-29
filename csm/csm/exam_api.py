import frappe
from frappe import db, whitelist
from ast import literal_eval


@frappe.whitelist()
def create_default_lists_for_exam(exam_id):
    exam_ban_list = db.exists("Exam Ban List", {"exam": exam_id})
    exam_exempt_list = db.exists("Exam Exempt List", {"exam": exam_id})
    exam_violated_list = db.exists("Exam Violated List", {"exam": exam_id})

    message = ""
    if not exam_ban_list:
        ban_list_doc = frappe.get_doc({
            "doctype": "Exam Ban List",
            "exam": exam_id
        })
        ban_list_doc.insert(ignore_permissions=True)
        message += f"ban_list_doc: {ban_list_doc.name}, "
    if not exam_exempt_list:
        exempt_list_doc = frappe.get_doc({
            "doctype": "Exam Exempt List",
            "exam": exam_id
        })
        exempt_list_doc.insert(ignore_permissions=True)
        message += f"exempt_list_doc: {exempt_list_doc.name}, "
    if not exam_violated_list:
        violated_list_doc = frappe.get_doc({
            "doctype": "Exam Violated List",
            "exam": exam_id
        })
        violated_list_doc.insert(ignore_permissions=True)
        message += f"violated_list_doc: {violated_list_doc.name}, "
    frappe.db.commit()

    print(f"Added documents: {message}")


def get_banned_students(exam_id):
    result = db.sql(f"""
        SELECT sl.student
        FROM `tabStudents List` sl
        JOIN `tabExam Ban List` ebl ON ebl.name = sl.parent AND sl.parenttype = "Exam Ban List"
        WHERE sl.parent = "{exam_id}"
    """, as_dict=True)
    return [item['student'] for item in result]


def get_exempted_students(exam_id):
    result = db.sql(f"""
        SELECT sl.student
        FROM `tabStudents List` sl
        JOIN `tabExam Exempt List` eel ON eel.name = sl.parent AND sl.parenttype = "Exam Exempt List"
        WHERE sl.parent = "{exam_id}"
    """, as_dict=True)
    return [item['student'] for item in result]


def get_banned_students(exam_id):
    result = db.sql(f"""
        SELECT sl.student
        FROM `tabStudents List` sl
        JOIN `tabExam Violated List` evl ON evl.name = sl.parent AND sl.parenttype = "Exam Violated List"
        WHERE sl.parent = "{exam_id}"
    """, as_dict=True)
    return [item['student'] for item in result]


@whitelist()
def check_students_in_ban_list(student_ids: list, exam_id):
    all_banned_students = get_banned_students(exam_id)
    result = []
    for student_id in literal_eval(student_ids):
        if student_id in all_banned_students:
            result.append(student_id)
    return result


@whitelist()
def check_students_in_exempt_list(student_ids: str, exam_id):
    all_exempted_students = get_exempted_students(exam_id)
    result = []
    for student_id in literal_eval(student_ids):
        if student_id in all_exempted_students:
            result.append(student_id)
    return result


@whitelist()
def remove_exempted_students_from_ban_list(exam_id):
    exempted_students = get_exempted_students(exam_id)
    all_banned_students = frappe.db.sql(f"""
        SELECT sl.student student_id, sl.name student_list_id
        FROM `tabStudents List` sl
        JOIN `tabExam Ban List` ebl ON ebl.name = sl.parent AND sl.parenttype = "Exam Ban List"
        WHERE ebl.exam = "{exam_id}"
    """, as_dict=True)

    removed_students = []
    for banned_students in all_banned_students:
        if banned_students['student_id'] in exempted_students:
            frappe.db.sql(f"""
                DELETE FROM `tabStudents List`
                WHERE name = "{banned_students['student_list_id']}"
            """)
            removed_students.append(banned_students['student_id'])
    frappe.db.commit()
    return removed_students


@whitelist()
def remove_banned_students_from_exempt_list(exam_id):
    banned_students = get_banned_students(exam_id)
    all_exempted_students = frappe.db.sql(f"""
        SELECT sl.student student_id, sl.name student_list_id
        FROM `tabStudents List` sl
        JOIN `tabExam Exempt List` ebl ON ebl.name = sl.parent AND sl.parenttype = "Exam Exempt List"
        WHERE ebl.exam = "{exam_id}"
    """, as_dict=True)

    removed_students = []
    for exempt_student in all_exempted_students:
        if exempt_student['student_id'] in banned_students:
            frappe.db.sql(f"""
                DELETE FROM `tabStudents List`
                WHERE name = "{exempt_student['student_list_id']}"
            """)
            removed_students.append(exempt_student['student_id'])
    frappe.db.commit()
    return removed_students
