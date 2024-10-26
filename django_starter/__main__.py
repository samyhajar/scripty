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
        base_installer = BaseInstaller()
        base_installer.welcome_message()
        base_installer.verify_env()

        django_installer = DjangoInstaller()
        django_installer.install()
        project_name = django_installer.setup_project()

        tailwind_installer = TailwindInstaller(project_name)
        tailwind_installer.install()

        template_creator = BaseTemplateCreator(project_name)
        template_creator.create_base_templates()

        app_creator = AppTemplateCreator(project_name)
        created_apps = app_creator.create_apps()

        django_installer.run_initial_setup()
        base_installer.show_next_steps(project_name, created_apps)

    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("Please try again or report this issue.")
        sys.exit(1)

if __name__ == "__main__":
    main()