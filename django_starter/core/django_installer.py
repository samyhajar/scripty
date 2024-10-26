# File: django_starter/core/django_installer.py

import subprocess
import sys
from pathlib import Path
from ..utils.validators import Validators

class DjangoInstaller:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.project_name = None
        self.validators = Validators()

    def install(self):
        """Install Django using pip."""
        print("\nInstalling Django...")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
            check=True
        )
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "django"],
            check=True
        )
        print("Django installed successfully!")

    def setup_project(self):
        """Set up Django project and return project name."""
        self.get_project_name()
        self.create_django_project()
        return self.project_name

    def get_project_name(self):
        """Get and validate project name from user input."""
        while True:
            name = input("\nEnter your project name: ").strip()
            if self.validators.is_valid_identifier(name):
                self.project_name = name
                break
            print("Project name must be a valid Python identifier")

    def create_django_project(self):
        """Create the Django project structure."""
        print(f"\nCreating Django project: {self.project_name}")
        subprocess.run(
            [
                sys.executable,
                "-m",
                "django",
                "startproject",
                self.project_name,
                str(self.base_dir),
            ],
            check=True,
        )
        print(f"Created Django project: {self.project_name}")

    def run_initial_setup(self):
        """Run initial Django setup including migrations and superuser creation."""
        print("\nRunning initial setup...")
        subprocess.run([sys.executable, "manage.py", "makemigrations"], check=True)
        subprocess.run([sys.executable, "manage.py", "migrate"], check=True)

        if input("\nWould you like to create a superuser? (y/n): ").lower() == "y":
            subprocess.run([sys.executable, "manage.py", "createsuperuser"], check=True)