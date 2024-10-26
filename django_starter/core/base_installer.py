# File: django_starter/core/base_installer.py

import os
import sys
from pathlib import Path
from ..utils.messages import Messages
from ..utils.validators import Validators

class BaseInstaller:
    def __init__(self):
        self.base_dir = Path.cwd()
        self.validators = Validators()
        self.messages = Messages()

    def welcome_message(self):
        """Display welcome message."""
        print(self.messages.WELCOME_MESSAGE)

    def verify_env(self):
        """Verify that we're running in a virtual environment."""
        if not sys.prefix == os.environ.get("VIRTUAL_ENV"):
            print(self.messages.VENV_ERROR)
            sys.exit(1)
        print("✓ Virtual environment verified!")

    def show_next_steps(self, project_name, created_apps):
        """Show next steps for the user."""
        print(self.messages.get_success_message(
            project_name,
            created_apps,
            self.base_dir
        ))