import frappe
from frappe.utils import get_assets_json
from frappe.tests.utils import FrappeTestCase
from werkzeug.wrappers import Response

from kustomize.api import (
	get_site_icon,
	inject_helpdesk_site_icon,
	update_website_context,
)


class TestKustomizeSettings(FrappeTestCase):
	def test_helpdesk_response_loads_custom_branding_script(self):
		response = Response(
			(
				"<html><head></head><body><script type='module' "
				"src='/assets/helpdesk/desk/assets/index.js'></script></body></html>"
			),
			mimetype="text/html",
		)
		request = frappe._dict(path="/helpdesk")

		inject_helpdesk_site_icon(response, request)

		self.assertIn(
			get_assets_json()["global.bundle.css"],
			response.get_data(as_text=True),
		)
		self.assertIn(
			get_assets_json()["helpdesk_branding.bundle.ts"],
			response.get_data(as_text=True),
		)

	def test_branding_is_applied_to_website_and_helpdesk(self):
		settings = frappe.get_single("Kustomize Settings")
		settings.site_name = "Kustomize Test Site"
		settings.slogan = "A test slogan"
		settings.logo = "/assets/frappe/images/frappe-framework-logo.svg"
		settings.favicon = "/assets/frappe/images/frappe-favicon.svg"
		settings.site_icon = "/files/uoe-icon.png"
		settings.save(ignore_permissions=True)
		colors = frappe.get_single("Kustomize Colors")
		colors.primary_color = "#112233"
		colors.brand_color = "#223344"
		colors.secondary_color = "#334455"
		colors.navbar_bg_color = "#445566"
		colors.action_color = "#556677"
		colors.sidebar_selector_color = "#667788"
		colors.sidebar_selector_text_color = "#778899"
		colors.heading_color = "#8899AA"
		colors.text_color = "#99AABB"
		colors.link_color = "#AABBCC"
		colors.action_hover_color = "#BBCCDD"
		colors.footer_color = "#CCDDEE"
		colors.save(ignore_permissions=True)

		self.assertEqual(
			frappe.db.get_single_value("Kustomize Settings", "site_icon"),
			settings.site_icon,
		)
		self.assertEqual(frappe.db.get_single_value("Website Settings", "app_name"), settings.site_name)
		self.assertEqual(frappe.db.get_single_value("Website Settings", "app_logo"), settings.logo)
		self.assertEqual(frappe.db.get_single_value("Website Settings", "favicon"), settings.favicon)
		self.assertEqual(
			frappe.db.get_single_value("Website Settings", "splash_image"),
			settings.site_icon,
		)
		self.assertEqual(get_site_icon()["logo"], settings.logo)
		self.assertEqual(get_site_icon()["site_icon"], settings.site_icon)
		self.assertEqual(
			get_site_icon()["colors"],
			{
				"primary_color": colors.primary_color,
				"brand_color": colors.brand_color,
				"secondary_color": colors.secondary_color,
				"navbar_bg_color": colors.navbar_bg_color,
				"action_color": colors.action_color,
				"sidebar_selector_color": colors.sidebar_selector_color,
				"sidebar_selector_text_color": colors.sidebar_selector_text_color,
				"heading_color": colors.heading_color,
				"text_color": colors.text_color,
				"link_color": colors.link_color,
				"action_hover_color": colors.action_hover_color,
				"footer_color": colors.footer_color,
			},
		)
		self.assertEqual(frappe.db.get_default("site_name"), settings.site_name)
		self.assertEqual(update_website_context(frappe._dict())["kustomize_slogan"], settings.slogan)

		if frappe.db.exists("DocType", "HD Settings"):
			self.assertEqual(frappe.db.get_single_value("HD Settings", "brand_name"), settings.site_name)
			self.assertEqual(
				frappe.db.get_single_value("HD Settings", "brand_logo"),
				settings.site_icon,
			)
			self.assertEqual(frappe.db.get_single_value("HD Settings", "favicon"), settings.favicon)
