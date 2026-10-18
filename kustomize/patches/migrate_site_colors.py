import frappe


COLOR_FIELDS = (
	"primary_color",
	"secondary_color",
	"header_color",
	"footer_color",
	"link_color",
	"action_color",
	"action_hover_color",
)


def execute():
	if not frappe.db.exists("DocType", "Kustomize Settings"):
		return

	for fieldname in COLOR_FIELDS:
		value = frappe.db.get_single_value("Kustomize Settings", fieldname)
		if value and not frappe.db.get_single_value("Kustomize Colors", fieldname):
			frappe.db.set_single_value(
				"Kustomize Colors",
				fieldname,
				value,
				update_modified=False,
			)
