### Kustomize

Reusable site branding and configuration for Frappe installations

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO
bench install-app kustomize
```

After installation, select **Kustomize** from Desk navigation and open **Site Branding** or **Site Colors** to configure them separately. Site Branding sets the public site name, logo, slogan, favicon, and site icon; Site Colors exposes only the `--kustomize-*` overrides for primary, brand, secondary, navbar, action, sidebar selection, heading, text, link, hover, and footer colors. The base palette and fallback values remain in `kustomize/public/scss/global/_colors.scss` and apply whenever an override is blank. The name is a display/branding value; it does not rename the site's domain or folder. Saving synchronizes the branding fields to Website Settings and, when Helpdesk is installed, its branding settings. The slogan is displayed on the login page; configured colors are applied to Frappe and Helpdesk interfaces. The shared stylesheet is `kustomize/public/scss/global.bundle.scss`; it imports global form styling from `global/_forms.scss`, and CSS variables are populated from Site Colors at runtime. Open Sans, Montserrat, and Raleway are self-hosted under `kustomize/public/fonts`, with their font licenses alongside the files.

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/kustomize
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
# frappe-kustomize-app
