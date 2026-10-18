import frappe
from frappe.utils import get_assets_json


@frappe.whitelist()
def get_site_icon():
	settings = frappe.get_single("Kustomize Settings")
	colors = frappe.get_single("Kustomize Colors")
	return {
		"logo": settings.logo or frappe.db.get_single_value("Website Settings", "app_logo") or "",
		"site_icon": settings.site_icon
		or frappe.db.get_single_value("Website Settings", "splash_image")
		or "",
		"colors": {
			fieldname: colors.get(fieldname) or ""
			for fieldname in (
				"primary_color",
				"brand_color",
				"secondary_color",
				"navbar_bg_color",
				"action_color",
				"sidebar_selector_color",
				"sidebar_selector_text_color",
				"heading_color",
				"text_color",
				"link_color",
				"action_hover_color",
				"footer_color",
			)
		},
	}


def inject_helpdesk_site_icon(response, request):
	if request.path != "/helpdesk" and not request.path.startswith("/helpdesk/"):
		return
	if response.mimetype != "text/html":
		return

	body = response.get_data()
	if b"/assets/helpdesk/desk/assets/" not in body:
		return

	assets = get_assets_json()
	stylesheet = assets.get("global.bundle.css")
	if stylesheet:
		link = f'<link rel="stylesheet" href="{stylesheet}">'.encode()
		if b"</head>" in body and link not in body:
			body = body.replace(b"</head>", link + b"</head>")

	# The Helpdesk SPA page does not include Frappe's web_include_js assets.
	script_asset = assets.get("helpdesk_branding.bundle.ts")
	if script_asset:
		script = f'<script src="{script_asset}"></script>'.encode()
		if b"</body>" in body and script not in body:
			body = body.replace(b"</body>", script + b"</body>")

	response.set_data(body)


def update_website_context(context):
	return {
		"kustomize_slogan": frappe.db.get_single_value("Kustomize Settings", "slogan") or "",
	}
