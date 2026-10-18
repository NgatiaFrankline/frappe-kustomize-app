import frappe
from frappe.model.document import Document


class KustomizeSettings(Document):
	def on_update(self):
		website_values = {
			"app_name": self.site_name or "",
			"app_logo": self.logo or "",
			"favicon": self.favicon or "",
			"splash_image": self.site_icon or self.logo or "",
		}
		for fieldname, value in website_values.items():
			frappe.db.set_single_value("Website Settings", fieldname, value)

		frappe.db.set_default("site_name", self.site_name or "")

		if frappe.db.exists("DocType", "HD Settings"):
			helpdesk_values = {
				"brand_name": self.site_name or "",
				"brand_logo": self.site_icon or self.logo or "",
				"favicon": self.favicon or "",
			}
			for fieldname, value in helpdesk_values.items():
				frappe.db.set_single_value("HD Settings", fieldname, value)

		frappe.get_doc("Website Settings").clear_cache()
		frappe.clear_cache()
