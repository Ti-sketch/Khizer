# Copyright (c) 2024, khizer and contributors
# For license information, please see license.txt

import frappe
from frappe.model.docstatus import DocStatus
from frappe.model.document import Document
from frappe.utils import add_days


class LibraryMembership(Document):
    def before_submit(self):
        if frappe.db.exists(
            "Library Membership",
            {
                "library_member": self.library_member,
                "to_date": (">", self.from_date),
                "docstatus": DocStatus.submitted(),
            },
        ):
            frappe.throw(
                f"Library Member {frappe.bold(self.library_member)} is already exists."
            )

        loan_period = frappe.db.get_single_value("Library Settings", "loan_period")
        self.to_date = add_days(self.from_date, loan_period or 30)
