interface SiteIconResponse {
  message?: {
    site_icon?: unknown;
    colors?: Record<string, unknown>;
  };
}

const logoSelector =
  ".fixed.z-50 .flex.flex-col.justify-center.items-center.gap-1.mt-4.mb-7 > svg";
let siteIcon = "";

function replaceOnboardingLogo(): void {
  if (!siteIcon) return;

  document.querySelectorAll<SVGElement>(logoSelector).forEach((logo) => {
    const image = document.createElement("img");
    image.src = siteIcon;
    image.alt = "Site icon";
    image.className = logo.getAttribute("class") || "";
    logo.replaceWith(image);
  });
}

const welcomeText = "Welcome to Frappe Helpdesk";
const customWelcomeText = "😊 Welcome!";
const colorVariables: Record<string, string> = {
  primary_color: "--kustomize-primary-color",
  brand_color: "--kustomize-brand-color",
  secondary_color: "--kustomize-secondary-color",
  navbar_bg_color: "--kustomize-navbar-bg-color",
  action_color: "--kustomize-action-color",
  sidebar_selector_color: "--kustomize-sidebar-selector-color",
  sidebar_selector_text_color: "--kustomize-sidebar-selector-text-color",
  heading_color: "--kustomize-heading-color",
  text_color: "--kustomize-text-color",
  link_color: "--kustomize-link-color",
  action_hover_color: "--kustomize-action-hover-color",
  footer_color: "--kustomize-footer-color",
};

function applySiteColors(colors: Record<string, unknown> = {}): void {
  const root = document.documentElement;
  Object.entries(colorVariables).forEach(([fieldname, variable]) => {
    const color = colors[fieldname];
    if (typeof color !== "string" || !CSS.supports("color", color)) return;
    root.style.setProperty(variable, color);
  });
}

function replaceWelcomeText(): void {
  document.querySelectorAll<HTMLElement>(".fixed.z-50 .text-base.font-medium").forEach((el) => {
    if (el.textContent?.trim() === welcomeText) el.textContent = customWelcomeText;
  });
}

function applyBranding(): void {
  replaceOnboardingLogo();
  replaceWelcomeText();
}

const observer = new MutationObserver(applyBranding);
observer.observe(document.body, { childList: true, subtree: true });

fetch("/api/method/kustomize.api.get_site_icon", {
  credentials: "same-origin",
})
  .then((response) => {
    if (!response.ok) {
      throw new Error(`Site icon request failed: ${response.status}`);
    }
    return response.json() as Promise<SiteIconResponse>;
  })
  .then((data) => {
    if (data.message && typeof data.message === "object") {
      if (typeof data.message.site_icon === "string") {
        siteIcon = data.message.site_icon;
      }
      applySiteColors(data.message.colors);
      applyBranding();
    }
  })
  .catch((error) => console.error("Unable to load the site icon.", error));
