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
            # 1. Install packages
            self.install_tailwind_package()

            # 2. Update initial settings with just tailwind
            self.update_initial_settings()

            # 3. Initialize tailwind app
            self.initialize_tailwind()

            # 4. Update settings with theme and browser reload
            self.update_final_settings()

            # 5. Run migrations
            self._run_migrations()

            # 6. Install tailwind dependencies
            self.install_dependencies()

            # 7. Build Tailwind CSS
            self.build_tailwind_css()

            print("\nTailwind CSS has been successfully installed and configured!")
        except Exception as e:
            raise Exception(f"Tailwind setup failed: {str(e)}")

    def install_tailwind_package(self):
        """Install Django Tailwind package."""
        print("\nInstalling Django Tailwind...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "django-tailwind[reload]"],
            check=True,
        )
        print("Django Tailwind installed successfully!")

    def update_initial_settings(self):
        """Add initial Tailwind configuration to settings."""
        with open(self.settings_path, "r") as file:
            content = file.readlines()

        self._add_import_os(content)

        # Add only tailwind to INSTALLED_APPS initially
        for i, line in enumerate(content):
            if "INSTALLED_APPS = [" in line:
                insert_index = i + 1
                content.insert(insert_index, "    'tailwind',\n")
                break

        with open(self.settings_path, "w") as file:
            file.writelines(content)
        print("Updated initial settings")

    def initialize_tailwind(self):
        """Initialize Tailwind with theme app."""
        print("\nInitializing Tailwind theme...")
        process = subprocess.Popen(
            [sys.executable, "manage.py", "tailwind", "init"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = process.communicate(input="theme\n")

        if process.returncode != 0:
            raise Exception(f"Failed to initialize Tailwind: {stderr}")
        print("Tailwind theme initialized successfully!")

    def update_final_settings(self):
        """Update settings after theme creation."""
        with open(self.settings_path, "r") as file:
            content = file.readlines()

        # Add theme and browser reload to INSTALLED_APPS
        for i, line in enumerate(content):
            if "INSTALLED_APPS = [" in line:
                insert_index = i + 1
                content.insert(insert_index, "    'theme',\n")
                content.insert(insert_index, "    'django_browser_reload',\n")
                break

        # Add browser reload middleware
        for i, line in enumerate(content):
            if "MIDDLEWARE = [" in line:
                content.insert(
                    i + 1,
                    '    "django_browser_reload.middleware.BrowserReloadMiddleware",\n',
                )
                break

        # Add Tailwind and IP configuration
        content.extend(
            [
                "\n# Tailwind configuration\n",
                "TAILWIND_APP_NAME = 'theme'\n",
                "\nINTERNAL_IPS = [\n",
                '    "127.0.0.1",\n',
                "]\n",
            ]
        )

        with open(self.settings_path, "w") as file:
            file.writelines(content)

        # Update urls.py
        self._update_urls()
        print("Updated final settings")

    def _update_urls(self):
        """Add browser reload URLs."""
        urls_path = self.base_dir / self.project_name / "urls.py"
        with open(urls_path, "r") as file:
            content = file.read()

        if "django_browser_reload" not in content:
            new_content = content.replace(
                "from django.urls import path", "from django.urls import path, include"
            )
            new_content = new_content.replace(
                "]\n",
                '    path("__reload__/", include("django_browser_reload.urls")),\n]\n',
            )

            with open(urls_path, "w") as file:
                file.write(new_content)

    def install_dependencies(self):
        """Install Tailwind dependencies."""
        print("\nInstalling Tailwind dependencies...")
        subprocess.run([sys.executable, "manage.py", "tailwind", "install"], check=True)
        print("Tailwind dependencies installed successfully!")

    def build_tailwind_css(self):
        """Build Tailwind CSS assets."""
        print("\nBuilding Tailwind CSS assets...")
        subprocess.run([sys.executable, "manage.py", "tailwind", "build"], check=True)
        print("Tailwind CSS assets built successfully!")

    def _run_migrations(self):
        """Run Django migrations."""
        print("\nRunning migrations...")
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)

    def _add_import_os(self, content):
        """Add OS import if not present."""
        if not any("import os" in line for line in content):
            content.insert(0, "import os\n")