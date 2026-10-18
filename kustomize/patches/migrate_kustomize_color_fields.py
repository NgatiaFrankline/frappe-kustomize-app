import frappe


def execute():
	if not frappe.db.exists("DocType", "Kustomize Colors"):
		return
	if not frappe.get_meta("Kustomize Colors").has_field("header_color"):
		return

	legacy_header_color = frappe.db.get_single_value("Kustomize Colors", "header_color")
	navbar_bg_color = frappe.db.sql(
		"SELECT value FROM `tabSingles` WHERE doctype = %s AND field = %s",
		("Kustomize Colors", "navbar_bg_color"),
	)
	navbar_bg_color = navbar_bg_color[0][0] if navbar_bg_color else None
	if legacy_header_color and not navbar_bg_color:
		frappe.db.set_single_value(
			"Kustomize Colors",
			"navbar_bg_color",
			legacy_header_color,
			update_modified=False,
		)
