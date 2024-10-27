# File: django_starter/templates/base_template_creator.py

from pathlib import Path

class BaseTemplateCreator:
    def __init__(self, project_name):
        self.base_dir = Path.cwd()
        self.project_name = project_name
        self.theme_templates = self.base_dir / "theme" / "templates"

    def create_base_templates(self):
        """Create base templates in the theme app."""
        self.theme_templates.mkdir(parents=True, exist_ok=True)
        self._create_base_html()
        self._create_navbar_partial()
        print("Base templates created successfully!")

    def _create_base_html(self):
        """Create the base.html template."""
        with open(self.theme_templates / "base.html", "w") as file:
            file.write(self._get_base_template())

    def _create_navbar_partial(self):
        """Create the navbar partial template."""
        partials_dir = self.theme_templates / "partials"
        partials_dir.mkdir(exist_ok=True)

        with open(partials_dir / "_navbar.html", "w") as file:
            file.write(self._get_navbar_template())

    def _get_base_template(self):
        """Return the content for base.html template."""
        return '''{% load static tailwind_tags %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}''' + self.project_name.capitalize() + '''{% endblock %}</title>
    {% tailwind_css %}
</head>
<body class="bg-gray-100 min-h-screen flex flex-col">
    <header class="bg-white shadow-lg">
        {% include "partials/_navbar.html" %}
    </header>

    <main class="container mx-auto px-4 py-8 flex-grow">
        {% block content %}{% endblock %}
    </main>

    <footer class="bg-gray-800 text-white mt-auto">
        <div class="container mx-auto px-4 py-6">
            <div class="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
                <p>&copy; {% now "Y" %} ''' + self.project_name.capitalize() + '''. All rights reserved.</p>
                <div class="flex space-x-6">
                    <a href="#" class="hover:text-gray-300 transition-colors">Privacy Policy</a>
                    <a href="#" class="hover:text-gray-300 transition-colors">Terms of Service</a>
                    <a href="#" class="hover:text-gray-300 transition-colors">Contact</a>
                </div>
            </div>
        </div>
    </footer>
</body>
</html>'''

    def _get_navbar_template(self):
        """Return the content for _navbar.html template."""
        return '''<nav class="container mx-auto px-4 py-4">
    <div class="flex flex-col md:flex-row md:justify-between md:items-center space-y-4 md:space-y-0">
        <div class="flex justify-between items-center">
            <a href="/" class="text-2xl font-bold text-gray-800 hover:text-gray-600 transition-colors">''' + self.project_name.capitalize() + '''</a>
            <button id="mobile-menu-button" class="md:hidden p-2 rounded hover:bg-gray-100 transition-colors">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
                </svg>
            </button>
        </div>
        <ul id="navbar-items" class="hidden md:flex flex-col md:flex-row space-y-4 md:space-y-0 md:space-x-8">
            <li><a href="/" class="text-gray-600 hover:text-gray-800 transition-colors">Home</a></li>
            {% block navigation %}
            {% endblock %}
        </ul>
    </div>
</nav>

<script>
    document.getElementById('mobile-menu-button').addEventListener('click', function() {
        const navItems = document.getElementById('navbar-items');
        navItems.classList.toggle('hidden');
    });
</script>'''