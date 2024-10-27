# File: django_starter/core/django_installer.py

import subprocess
import sys
from pathlib import Path
from ..utils.validators import Validators

class DjangoInstaller:
    def __init__(self):
        self.validators = Validators()
        self.project_name = None
        self.main_app_name = None

    def get_project_name(self):
        """Get and validate project name from user input."""
        while True:
            name = input("\nEnter your project name: ").strip()
            if self.validators.is_valid_identifier(name):
                self.project_name = name
                return name
            print("Project name must be a valid Python identifier")

    def get_main_app_name(self):
        """Get and validate main app name from user input."""
        while True:
            name = input("\nEnter your main app name (this will be your homepage): ").strip()
            if self.validators.is_valid_identifier(name):
                self.main_app_name = name
                return name
            print("App name must be a valid Python identifier")

    def create_django_project(self, project_dir):
        """Create the Django project structure."""
        print(f"\nCreating Django project: {self.project_name}")
        subprocess.run(
            [
                sys.executable,
                "-m",
                "django",
                "startproject",
                self.project_name,
                str(project_dir),
            ],
            check=True,
        )
        print(f"Created Django project: {self.project_name}")

    def configure_main_app_routing(self, main_app_name):
        """Configure main app as homepage."""
        settings_path = Path.cwd() / self.project_name / "settings.py"
        urls_path = Path.cwd() / self.project_name / "urls.py"

        # Update settings.py
        with open(settings_path, "r") as f:
            content = f.readlines()

        for i, line in enumerate(content):
            if "ROOT_URLCONF = " in line:
                content.insert(i + 1, f"HOME_APP = '{main_app_name}'\n")
                break

        with open(settings_path, "w") as f:
            f.writelines(content)

        # Update urls.py to make main app the homepage
        with open(urls_path, "r") as f:
            content = f.read()

        new_content = f'''from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', include(f"{{settings.HOME_APP}}.urls")),
]
'''
        with open(urls_path, "w") as f:
            f.write(new_content)

    def run_initial_setup(self):
        """Run initial Django setup including migrations and superuser creation."""
        print("\nRunning initial setup...")
        subprocess.run([sys.executable, "manage.py", "makemigrations"], check=True)
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)

        if input("\nWould you like to create a superuser? (y/n): ").lower() == "y":
            subprocess.run([sys.executable, "manage.py", "createsuperuser"], check=True)