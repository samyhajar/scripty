# File: django_starter/templates/app_template_creator.py

import sys
import subprocess
from pathlib import Path

class AppTemplateCreator:
    def __init__(self, project_name):
        self.base_dir = Path.cwd()
        self.project_name = project_name
        self.created_apps = []

    def create_apps(self):
        """Create multiple apps based on user input."""
        print("\nEnter the names of the apps you want to create (separated by spaces):")
        apps_input = input().strip()

        if apps_input:
            app_names = [app.strip() for app in apps_input.split()]
            for app_name in app_names:
                if app_name.isidentifier():
                    self.created_apps.append(app_name)
                    print(f"\nCreating app: {app_name}")
                    self._create_app(app_name)
                else:
                    print(f"Skipping invalid app name: {app_name}")

            self._update_settings_with_apps()
            self._update_main_urls()
            print("\nAll apps created successfully!")

        return self.created_apps

    def _create_app(self, app_name):
        """Create a single app with all necessary files."""
        subprocess.run(
            [sys.executable, "manage.py", "startapp", app_name],
            check=True
        )
        self._create_app_files(app_name)
        self._create_templates_structure(app_name)

    def _create_app_files(self, app_name):
        """Create necessary files for the app."""
        app_dir = self.base_dir / app_name

        # Create urls.py
        with open(app_dir / "urls.py", "w") as file:
            file.write(self._get_urls_template(app_name))

        # Create views.py
        with open(app_dir / "views.py", "w") as file:
            file.write(self._get_views_template(app_name))

        # Create models.py
        with open(app_dir / "models.py", "w") as file:
            file.write(self._get_models_template(app_name))

        # Create admin.py
        with open(app_dir / "admin.py", "w") as file:
            file.write(self._get_admin_template(app_name))

    def _create_templates_structure(self, app_name):
        """Create templates structure for both the app and theme."""
        # Create app-specific templates directory
        app_templates = self.base_dir / app_name / "templates" / "pages" / app_name
        app_templates.mkdir(parents=True, exist_ok=True)

        # Create theme templates directory for the app
        theme_templates = self.base_dir / "theme" / "templates" / "pages" / app_name
        theme_templates.mkdir(parents=True, exist_ok=True)

        # Create templates
        templates = {
            "index.html": self._get_index_template(app_name),
            "about.html": self._get_about_template(app_name)
        }

        # Create templates in both locations
        for template_name, content in templates.items():
            with open(app_templates / template_name, "w") as file:
                file.write(content)
            with open(theme_templates / template_name, "w") as file:
                file.write(content)

    def _update_settings_with_apps(self):
        """Update settings.py to include the created apps."""
        settings_path = self.base_dir / self.project_name / "settings.py"
        with open(settings_path, "r") as file:
            content = file.readlines()

        for i, line in enumerate(content):
            if "INSTALLED_APPS = [" in line:
                insert_index = i
                while "]" not in content[insert_index]:
                    insert_index += 1
                for app in self.created_apps:
                    content.insert(insert_index, f"    '{app}',\n")
                break

        with open(settings_path, "w") as file:
            file.writelines(content)

    def _update_main_urls(self):
        """Update the main urls.py to include app URLs."""
        urls_path = self.base_dir / self.project_name / "urls.py"
        with open(urls_path, "w") as file:
            file.write(self._get_main_urls_template())

    def _get_urls_template(self, app_name):
        """Generate urls.py content for the app."""
        return f'''from django.urls import path
from . import views

app_name = "{app_name}"

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
]
'''

    def _get_views_template(self, app_name):
        """Generate views.py content for the app."""
        return f'''from django.shortcuts import render

def index(request):
    context = {{
        "title": "{app_name.capitalize()} Home",
        "project_name": "{self.project_name}"
    }}
    return render(request, "pages/{app_name}/index.html", context)

def about(request):
    context = {{
        "title": "About {app_name.capitalize()}",
        "project_name": "{self.project_name}"
    }}
    return render(request, "pages/{app_name}/about.html", context)
'''

    def _get_models_template(self, app_name):
        """Generate models.py content for the app."""
        return f'''from django.db import models

class {app_name.capitalize()}Item(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "{app_name.capitalize()} Item"
        verbose_name_plural = "{app_name.capitalize()} Items"
'''

    def _get_admin_template(self, app_name):
        """Generate admin.py content for the app."""
        return f'''from django.contrib import admin
from .models import {app_name.capitalize()}Item

@admin.register({app_name.capitalize()}Item)
class {app_name.capitalize()}ItemAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "updated_at")
    search_fields = ("title", "description")
    list_filter = ("created_at", "updated_at")
'''

    def _get_main_urls_template(self):
        """Generate main urls.py content."""
        content = '''from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
'''
        for app in self.created_apps:
            content += f'    path("{app}/", include("{app}.urls", namespace="{app}")),\n'
        content += "]\n"
        return content

    def _get_index_template(self, app_name):
        """Generate index.html template for the app."""
        return '''{% extends "base.html" %}

{% block title %}''' + f"{app_name.capitalize()}" + ''' Home{% endblock %}

{% block navigation %}
    {{ block.super }}
    <li><a href="{% url "''' + f"{app_name}:index" + '''" %}" class="hover:text-blue-200 transition-colors">''' + f"{app_name.capitalize()}" + '''</a></li>
    <li><a href="{% url "''' + f"{app_name}:about" + '''" %}" class="hover:text-blue-200 transition-colors">About ''' + f"{app_name.capitalize()}" + '''</a></li>
{% endblock %}

{% block content %}
    <div class="bg-white shadow-md rounded-lg p-6">
        <h1 class="text-3xl font-bold text-gray-800 mb-4">Welcome to ''' + f"{app_name.capitalize()}" + '''</h1>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="bg-blue-50 p-4 rounded-lg">
                <h2 class="text-xl font-semibold text-blue-800 mb-2">Features</h2>
                <ul class="list-disc list-inside text-blue-600">
                    <li>Feature 1</li>
                    <li>Feature 2</li>
                    <li>Feature 3</li>
                </ul>
            </div>

            <div class="bg-green-50 p-4 rounded-lg">
                <h2 class="text-xl font-semibold text-green-800 mb-2">Statistics</h2>
                <ul class="list-disc list-inside text-green-600">
                    <li>Stat 1</li>
                    <li>Stat 2</li>
                    <li>Stat 3</li>
                </ul>
            </div>
        </div>
    </div>
{% endblock %}'''

    def _get_about_template(self, app_name):
        """Generate about.html template for the app."""
        return '''{% extends "base.html" %}

{% block title %}About ''' + f"{app_name.capitalize()}" + '''{% endblock %}

{% block navigation %}
    {{ block.super }}
    <li><a href="{% url "''' + f"{app_name}:index" + '''" %}" class="hover:text-blue-200 transition-colors">''' + f"{app_name.capitalize()}" + '''</a></li>
    <li><a href="{% url "''' + f"{app_name}:about" + '''" %}" class="hover:text-blue-200 transition-colors">About ''' + f"{app_name.capitalize()}" + '''</a></li>
{% endblock %}

{% block content %}
    <div class="bg-white shadow-md rounded-lg p-6">
        <h1 class="text-3xl font-bold text-gray-800 mb-4">About ''' + f"{app_name.capitalize()}" + '''</h1>

        <div class="space-y-6">
            <div class="bg-gray-50 p-4 rounded-lg">
                <h2 class="text-xl font-semibold text-gray-800 mb-2">Our Mission</h2>
                <p class="text-gray-600">
                    This is a sample about page for the ''' + f"{app_name}" + ''' application.
                    Replace this content with your actual mission statement.
                </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="bg-blue-50 p-4 rounded-lg">
                    <h3 class="text-lg font-semibold text-blue-800 mb-2">Section 1</h3>
                    <p class="text-blue-600">Content for section 1</p>
                </div>

                <div class="bg-green-50 p-4 rounded-lg">
                    <h3 class="text-lg font-semibold text-green-800 mb-2">Section 2</h3>
                    <p class="text-green-600">Content for section 2</p>
                </div>

                <div class="bg-purple-50 p-4 rounded-lg">
                    <h3 class="text-lg font-semibold text-purple-800 mb-2">Section 3</h3>
                    <p class="text-purple-600">Content for section 3</p>
                </div>``
            </div>
        </div>
    </div>
{% endblock %}'''