# File: django_starter/core/tailwind_installer.py

import subprocess
import sys
from pathlib import Path

class TailwindInstaller:
    def __init__(self, project_name):
        self.base_dir = Path.cwd()
        self.project_name = project_name
        self.settings_path = self.base_dir / project_name / "settings.py"

    def install(self):
        """Main installation method."""
        try:
            self.install_tailwind_package()
            self.update_settings()
            self.initialize_tailwind()
            self.install_browser_reload()
            self.install_dependencies()
            print("\nTailwind CSS has been successfully installed and configured!")
        except Exception as e:
            raise Exception(f"Tailwind setup failed: {str(e)}")

    def install_tailwind_package(self):
        """Install Django Tailwind package."""
        print("\nInstalling Django Tailwind...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "django-tailwind[reload]"],
            check=True
        )
        print("Django Tailwind installed successfully!")

    def update_settings(self):
        """Update Django settings for Tailwind."""
        with open(self.settings_path, "r") as file:
            content = file.readlines()

        self._add_import_os(content)
        self._add_tailwind_apps(content)
        self._add_tailwind_config(content)
        self._update_middleware(content)
        self._update_templates(content)

        with open(self.settings_path, "w") as file:
            file.writelines(content)
        print("Updated settings configuration")

    def initialize_tailwind(self):
        """Initialize Tailwind theme app."""
        print("\nInitializing Tailwind...")
        process = subprocess.Popen(
            [sys.executable, "manage.py", "tailwind", "init"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = process.communicate(input="theme\n")

        if process.returncode != 0:
            raise Exception(f"Tailwind initialization failed: {stderr}")
        print("Tailwind theme app created successfully!")

    def install_browser_reload(self):
        """Install django-browser-reload package."""
        print("\nInstalling django-browser-reload...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "django-browser-reload"],
            check=True
        )
        print("Browser reload installed successfully!")

    def install_dependencies(self):
        """Install Tailwind dependencies."""
        print("\nInstalling Tailwind dependencies...")
        subprocess.run(
            [sys.executable, "manage.py", "tailwind", "install"],
            check=True
        )
        print("Tailwind dependencies installed successfully!")

    # Private helper methods
    def _add_import_os(self, content):
        """Add OS import if not present."""
        if "import os" not in content[0]:
            content.insert(0, "import os\n")

    def _add_tailwind_apps(self, content):
        """Add Tailwind apps to INSTALLED_APPS."""
        for i, line in enumerate(content):
            if "INSTALLED_APPS = [" in line:
                insert_index = i
                while "]" not in content[insert_index]:
                    insert_index += 1
                content.insert(insert_index, "    'tailwind',\n")
                content.insert(insert_index, "    'theme',\n")
                content.insert(insert_index, "    'django_browser_reload',\n")
                break

    def _add_tailwind_config(self, content):
        """Add Tailwind configuration settings."""
        content.append("\n# Tailwind configuration\n")
        content.append("TAILWIND_APP_NAME = 'theme'\n")
        content.append("\nINTERNAL_IPS = [\n")
        content.append('    "127.0.0.1",\n')
        content.append("]\n")

    def _update_middleware(self, content):
        """Add browser reload middleware."""
        for i, line in enumerate(content):
            if "MIDDLEWARE = [" in line:
                content.insert(
                    i + 1,
                    '    "django_browser_reload.middleware.BrowserReloadMiddleware",\n'
                )
                break

    def _update_templates(self, content):
        """Ensure APP_DIRS is True in templates."""
        for i, line in enumerate(content):
            if "TEMPLATES = [" in line:
                insert_index = i
                while "]" not in content[insert_index]:
                    insert_index += 1
                    if "'APP_DIRS': True," in content[insert_index]:
                        break
                else:
                    content.insert(insert_index, "        'APP_DIRS': True,\n")
                break