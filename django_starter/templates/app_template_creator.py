import sys
import subprocess
from pathlib import Path
from .template_generators.admin_templates import get_admin_template
from .template_generators.view_templates import get_views_template
from .template_generators.model_templates import get_models_template
from .template_generators.url_templates import get_urls_template
from .template_generators.html_templates import (
    get_main_index_template,
    get_index_template,
    get_about_template
)

class AppTemplateCreator:
    def __init__(self, project_name):
        self.base_dir = Path.cwd()
        self.project_name = project_name
        self.created_apps = []
        self.main_app = 'home'  # Fixed main app name

    def create_apps(self):
        """Create main app and additional apps."""
        # Create main app (home) first
        print(f"\nCreating main app: {self.main_app}")
        self.created_apps.append(self.main_app)
        self._create_app(self.main_app, is_main=True)

        # Create required apps (clients and orders)
        required_apps = ['clients', 'orders']
        for app_name in required_apps:
            self.created_apps.append(app_name)
            print(f"\nCreating app: {app_name}")
            self._create_app(app_name, is_main=False)

        # Ask for additional apps
        while True:
            additional_app = input("\nEnter additional app name (or press Enter to finish): ").strip().lower()
            if not additional_app:
                break
            if additional_app in self.created_apps:
                print(f"App {additional_app} already exists. Please enter a different name.")
                continue
            if additional_app in ['admin', 'auth', 'contenttypes', 'sessions']:
                print(f"Cannot create app named {additional_app} as it conflicts with Django's internal apps.")
                continue
            self.created_apps.append(additional_app)
            print(f"\nCreating app: {additional_app}")
            self._create_app(additional_app, is_main=False)

        self._update_settings_with_apps()
        self._update_main_urls()
        print("\nAll apps created successfully!")
        return self.created_apps

    def _create_app(self, app_name, is_main=False):
        """Create a single app with all necessary files."""
        subprocess.run(
            [sys.executable, "manage.py", "startapp", app_name],
            check=True
        )
        self._create_app_files(app_name, is_main)
        self._create_templates_structure(app_name, is_main)

    def _create_app_files(self, app_name, is_main):
        """Create necessary files for the app."""
        app_dir = self.base_dir / app_name

        # Create urls.py
        with open(app_dir / "urls.py", "w") as file:
            file.write(get_urls_template(app_name))

        # Create views.py
        with open(app_dir / "views.py", "w") as file:
            file.write(get_views_template(app_name, self.project_name, is_main))

        # Create models.py
        with open(app_dir / "models.py", "w") as file:
            file.write(get_models_template(app_name))

        # Create admin.py with appropriate configurations
        list_display = self._get_list_display(app_name)
        search_fields = self._get_search_fields(app_name)
        list_filter = self._get_list_filter(app_name)
        model_name = self._get_model_name(app_name)

        with open(app_dir / "admin.py", "w") as file:
            file.write(get_admin_template(
                app_name,
                model_name,
                list_display,
                search_fields,
                list_filter,
                is_main_app=(app_name == self.main_app)
            ))

    def _create_templates_structure(self, app_name, is_main):
        """Create templates structure for the app."""
        templates_dir = self.base_dir / app_name / "templates" / app_name
        templates_dir.mkdir(parents=True, exist_ok=True)

        if is_main:
            with open(templates_dir / "index.html", "w") as file:
                file.write(get_main_index_template())
            with open(templates_dir / "about.html", "w") as file:
                file.write(get_about_template(app_name))
        else:
            with open(templates_dir / "index.html", "w") as file:
                file.write(get_index_template(app_name))
            with open(templates_dir / "about.html", "w") as file:
                file.write(get_about_template(app_name))

    def _update_settings_with_apps(self):
        """Update settings.py to include the created apps."""
        settings_path = self.base_dir / self.project_name / "settings.py"
        with open(settings_path, "r") as file:
            content = file.readlines()

        for i, line in enumerate(content):
            if "INSTALLED_APPS = [" in line:
                insert_index = i + 1
                while "]" not in content[insert_index]:
                    insert_index += 1
                for app in self.created_apps:
                    content.insert(insert_index, f"    '{app}',\n")
                break

        with open(settings_path, "w") as file:
            file.writelines(content)

    def _update_main_urls(self):
        """Update the main urls.py to include app URLs."""
        urls_path = self.base_dir / self.project_name / "urls.py"
        content = f"""from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__reload__/', include('django_browser_reload.urls')),
    path('', include('{self.main_app}.urls')),  # Main app as homepage
"""
        # Add other apps with their own URL prefixes
        for app in self.created_apps:
            if app != self.main_app:
                content += f'    path("{app}/", include("{app}.urls", namespace="{app}")),\n'

        content += "]\n"

        with open(urls_path, "w") as file:
            file.write(content)

    def _get_model_name(self, app_name):
        """Get the model name for an app."""
        if app_name == "clients":
            return "Client"
        elif app_name == "orders":
            return "Order"
        else:
            return f"{app_name.capitalize()}Item"

    def _get_list_display(self, app_name):
        """Get list_display fields for admin."""
        if app_name == "clients":
            return '("first_name", "last_name", "email", "phone_number")'
        elif app_name == "orders":
            return '("client", "order_date", "delivery_date", "total_amount", "status")'
        else:
            return '("title", "created_at", "updated_at")'

    def _get_search_fields(self, app_name):
        """Get search_fields for admin."""
        if app_name == "clients":
            return '("first_name", "last_name", "email")'
        elif app_name == "orders":
            return '("client__first_name", "client__last_name", "status")'
        else:
            return '("title", "description")'

    def _get_list_filter(self, app_name):
        """Get list_filter fields for admin."""
        if app_name == "clients":
            return '("email",)'
        elif app_name == "orders":
            return '("order_date", "status")'
        else:
            return '("created_at", "updated_at")'