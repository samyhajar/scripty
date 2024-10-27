import subprocess
import sys
from pathlib import Path
from ..utils.validators import Validators
from ..utils.timezone_selector import TimezoneSelector

class DjangoInstaller:
    def __init__(self):
        self.validators = Validators()
        self.project_name = None
        self.main_app_name = 'home'  # Fixed main app name
        self.timezone_selector = TimezoneSelector()

    def get_project_name(self):
        """Get and validate project name from user input."""
        while True:
            name = input("\nEnter your project name: ").strip()
            if self.validators.is_valid_identifier(name):
                self.project_name = name
                return name
            print("Project name must be a valid Python identifier")

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

        # Select and configure timezone
        print("\nConfiguring timezone...")
        timezone = self.timezone_selector.select_timezone()
        self.timezone_selector.update_settings(self.project_name, timezone)
        print(f"Created Django project: {self.project_name} with timezone {timezone}")

    def configure_main_app_routing(self):
        """Configure home app as homepage."""
        settings_path = Path.cwd() / self.project_name / "settings.py"
        urls_path = Path.cwd() / self.project_name / "urls.py"

        # Update settings.py
        with open(settings_path, "r") as f:
            content = f.readlines()

        for i, line in enumerate(content):
            if "ROOT_URLCONF = " in line:
                content.insert(i + 1, f"HOME_APP = '{self.main_app_name}'\n")
                break

        # Update Django settings
        updated_settings = []
        in_i18n_section = False
        for line in content:
            if '# Internationalization' in line:
                in_i18n_section = True
            if in_i18n_section and line.strip() == '':
                in_i18n_section = False
            if not in_i18n_section:
                updated_settings.append(line)
            elif 'LANGUAGE_CODE =' not in line and 'TIME_ZONE =' not in line:
                updated_settings.append(line)

        with open(settings_path, "w") as f:
            f.writelines(updated_settings)

        # Update urls.py to make home app the homepage
        with open(urls_path, "w") as f:
            f.write('''from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', include(f"{settings.HOME_APP}.urls")),
]
''')

    def configure_default_settings(self):
        """Configure default settings for the project."""
        settings_path = Path.cwd() / self.project_name / "settings.py"

        # Read current settings
        with open(settings_path, "r") as f:
            content = f.readlines()

        # Find the Internationalization section and update it
        i18n_settings = """
# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_TZ = True

"""
        # Update settings content
        updated_content = []
        skip_lines = 0
        for i, line in enumerate(content):
            if skip_lines > 0:
                skip_lines -= 1
                continue
            if '# Internationalization' in line:
                updated_content.append(i18n_settings)
                # Skip existing i18n settings
                skip_lines = 5  # Adjust this number based on your default settings structure
            else:
                updated_content.append(line)

        # Write updated settings
        with open(settings_path, "w") as f:
            f.writelines(updated_content)

    def run_initial_setup(self):
        """Run initial Django setup including migrations and superuser creation."""
        print("\nRunning initial setup...")
        subprocess.run([sys.executable, "manage.py", "makemigrations"], check=True)
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)

        if input("\nWould you like to create a superuser? (y/n): ").lower() == "y":
            subprocess.run([sys.executable, "manage.py", "createsuperuser"], check=True)