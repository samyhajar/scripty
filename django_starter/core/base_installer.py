# File: django_starter/core/base_installer.py

import os
import sys
import shutil
from pathlib import Path
from ..utils.messages import Messages
from ..utils.validators import Validators

class BaseInstaller:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.validators = Validators()
        self.messages = Messages()
        self.projects_dir = self.base_dir / "django_projects"

    def welcome_message(self):
        print(self.messages.WELCOME_MESSAGE)

    def verify_env(self):
        if not sys.prefix == os.environ.get("VIRTUAL_ENV"):
            print(self.messages.VENV_ERROR)
            sys.exit(1)
        print("✓ Virtual environment verified!")

    def cleanup(self):
        """Clean up previous projects."""
        print("\nCleaning up previous projects...")
        if self.projects_dir.exists():
            shutil.rmtree(self.projects_dir)
        self.projects_dir.mkdir(exist_ok=True)
        print("Cleanup completed!")

    def setup_project_directory(self, project_name):
        """Create and set up project directory."""
        project_dir = self.projects_dir / project_name
        project_dir.mkdir(parents=True, exist_ok=True)
        os.chdir(project_dir)
        return project_dir

    def show_next_steps(self, project_name, created_apps):
        """Show next steps for the user."""
        print(self.messages.get_success_message(
            project_name,
            created_apps,
            self.projects_dir / project_name
        ))