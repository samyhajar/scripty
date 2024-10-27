# File: django_starter/__main__.py

import sys
from pathlib import Path
from . import (
    BaseInstaller,
    DjangoInstaller,
    TailwindInstaller,
    BaseTemplateCreator,
    AppTemplateCreator,
)

def main():
    try:
        # Initialize installers
        base_installer = BaseInstaller()
        base_installer.welcome_message()
        base_installer.verify_env()

        # Cleanup previous projects
        base_installer.cleanup()

        # Get project and app names first
        django_installer = DjangoInstaller()
        project_name = django_installer.get_project_name()
        app_name = django_installer.get_main_app_name()

        # Setup project directory
        project_dir = base_installer.setup_project_directory(project_name)

        # Create Django project
        django_installer.create_django_project(project_dir)

        # Install and configure Tailwind
        tailwind_installer = TailwindInstaller(project_name)
        tailwind_installer.install()

        # Create base templates
        template_creator = BaseTemplateCreator(project_name)
        template_creator.create_base_templates()

        # Create main app and additional apps
        app_creator = AppTemplateCreator(project_name)
        created_apps = app_creator.create_apps(main_app=app_name)

        # Set up URL routing
        django_installer.configure_main_app_routing(app_name)

        # Run initial setup
        django_installer.run_initial_setup()

        base_installer.show_next_steps(project_name, created_apps)

    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("Please try again or report this issue.")
        sys.exit(1)

if __name__ == "__main__":
    main()