# File: django_starter/utils/messages.py


class Messages:
    WELCOME_MESSAGE = """
╔══════════════════════════════════════════╗
║         Django Project Starter           ║
╚══════════════════════════════════════════╝

Assuming your virtual environment is already activated!
"""

    VENV_ERROR = """
❌ Virtual environment is not activated!

Please activate your virtual environment first:
- Windows: .venv\\Scripts\\activate
- Unix/MacOS: source .venv/bin/activate

Then run this script again.
"""

    @staticmethod
    def get_success_message(project_name, created_apps, base_dir):
        return f"""
✨ Project successfully created! ✨

Your project is ready! Next steps:

1. Start the development server:
   python manage.py runserver

2. In a separate terminal, start Tailwind development server:
   python manage.py tailwind start

Your project is ready at: {base_dir}
Created apps: {', '.join(created_apps) if created_apps else 'None'}

Happy coding! 🚀
"""
