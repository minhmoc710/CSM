import frappe
from frappe import db, whitelist


@whitelist()
def find_users_with_roles(child_table_id: str, parent_id: str, user_id_field: str, role_field: str, role: str) -> list:
    """
    Return list of user_id with certain role in a child table
    """
    return db.get_all(child_table_id, {"parent": parent_id, role_field: role}, [user_id_field], pluck=user_id_field)


@whitelist()
def set_user_permission_for_doc(user_ids: list, allow: str, for_value: str):
    """
    allow: The doctype name
    for_value: The document id
    """
    delete_all_permission_for_doc(allow, for_value)
    for user_id in user_ids:
        user_permission_doc = frappe.get_doc({
            "doctype": "User Permission",
            "user": user_id,
            "allow": allow,
            "for_value": for_value
        })
        user_permission_doc.insert(ignore_permissions=True)
        frappe.db.commit()


def delete_all_permission_for_doc(allow: str, for_value: str):
    """
    Delete all "User Permission" for a certain document
    allow: The doctype name
    for_value: The document id
    """
    all_user_permissions = db.get_all("User Permission", { "allow": allow, "for_value": for_value }, pluck="name")
    for user_permission in all_user_permissions:
        db.delete("User Permission", {"name": user_permission})
    frappe.db.commit()