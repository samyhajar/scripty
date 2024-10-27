# File: django_starter/templates/app_template_creator.py

import sys
import subprocess
from pathlib import Path

class AppTemplateCreator:
    def __init__(self, project_name):
        self.base_dir = Path.cwd()
        self.project_name = project_name
        self.created_apps = []

    def create_apps(self, main_app):
        """Create main app and additional apps."""
        # Create main app first
        print(f"\nCreating main app: {main_app}")
        self.created_apps.append(main_app)
        self._create_app(main_app, is_main=True)

        # Create additional apps
        print("\nEnter additional app names (separated by spaces), or press Enter to skip:")
        apps_input = input().strip()

        if apps_input:
            app_names = [app.strip() for app in apps_input.split()]
            for app_name in app_names:
                if app_name.isidentifier() and app_name != main_app:
                    self.created_apps.append(app_name)
                    print(f"\nCreating app: {app_name}")
                    self._create_app(app_name, is_main=False)
                else:
                    print(f"Skipping invalid app name: {app_name}")

        self._update_settings_with_apps()
        self._update_main_urls(main_app)
        print("\nAll apps created successfully!")
        return self.created_apps

    def _create_app(self, app_name, is_main=False):
        """Create a single app with all necessary files."""
        subprocess.run(
            [sys.executable, "manage.py", "startapp", app_name],
            check=True
        )
        self._create_app_files(app_name, is_main)
        self._create_templates_structure(app_name, is_main)

    def _create_app_files(self, app_name, is_main):
        """Create necessary files for the app."""
        app_dir = self.base_dir / app_name

        # Create urls.py
        with open(app_dir / "urls.py", "w") as file:
            file.write(self._get_urls_template(app_name))

        # Create views.py
        with open(app_dir / "views.py", "w") as file:
            file.write(self._get_views_template(app_name, is_main))

        # Create models.py
        with open(app_dir / "models.py", "w") as file:
            file.write(self._get_models_template(app_name))

        # Create admin.py
        with open(app_dir / "admin.py", "w") as file:
            file.write(self._get_admin_template(app_name))

    def _create_templates_structure(self, app_name, is_main):
        """Create templates structure for the app."""
        templates_dir = self.base_dir / app_name / "templates" / app_name
        templates_dir.mkdir(parents=True, exist_ok=True)

        if is_main:
            # For main app, create index.html for homepage
            with open(templates_dir / "index.html", "w") as file:
                file.write(self._get_main_index_template())
        else:
            # For other apps, create standard templates
            with open(templates_dir / "index.html", "w") as file:
                file.write(self._get_index_template(app_name))
            with open(templates_dir / "about.html", "w") as file:
                file.write(self._get_about_template(app_name))

    def _update_settings_with_apps(self):
        """Update settings.py to include the created apps."""
        settings_path = self.base_dir / self.project_name / "settings.py"
        with open(settings_path, "r") as file:
            content = file.readlines()

        for i, line in enumerate(content):
            if "INSTALLED_APPS = [" in line:
                insert_index = i + 1
                while "]" not in content[insert_index]:
                    insert_index += 1
                for app in self.created_apps:
                    content.insert(insert_index, f"    '{app}',\n")
                break

        with open(settings_path, "w") as file:
            file.writelines(content)

    def _update_main_urls(self, main_app):
        """Update the main urls.py to include app URLs."""
        urls_path = self.base_dir / self.project_name / "urls.py"
        content = f"""from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__reload__/', include('django_browser_reload.urls')),
    path('', include('{main_app}.urls')),  # Main app as homepage
"""

        # Add other apps with their own URL prefixes
        for app in self.created_apps:
            if app != main_app:
                content += f'    path("{app}/", include("{app}.urls", namespace="{app}")),\n'

        content += "]\n"

        with open(urls_path, "w") as file:
            file.write(content)

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

    def _get_views_template(self, app_name, is_main):
        """Generate views.py content for the app."""
        return f'''from django.shortcuts import render

def index(request):
    context = {{
        "title": "Welcome to {self.project_name.capitalize()}" if {is_main} else "{app_name.capitalize()} Home",
        "project_name": "{self.project_name}"
    }}
    return render(request, "{app_name}/index.html", context)

def about(request):
    context = {{
        "title": "About {app_name.capitalize()}",
        "project_name": "{self.project_name}"
    }}
    return render(request, "{app_name}/about.html", context)
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
from unfold.admin import ModelAdmin

# Unregister the model if already registered
try:
    admin.site.unregister({app_name.capitalize()}Item)
except admin.sites.NotRegistered:
    pass

@admin.register({app_name.capitalize()}Item)
class {app_name.capitalize()}ItemAdmin(ModelAdmin):
    list_display = ("title", "created_at", "updated_at")
    search_fields = ("title", "description")
    list_filter = ("created_at", "updated_at")
'''

    def _get_main_index_template(self):
        """Generate main index.html template for homepage."""
        return '''{% extends "base.html" %}

{% block title %}Welcome to {{ project_name|capfirst }}{% endblock %}

{% block content %}
<div class="max-w-4xl mx-auto">
    <!-- Hero Section -->
    <div class="bg-white rounded-lg shadow-md p-8 mb-8">
        <h1 class="text-4xl font-bold text-gray-800 mb-4">Welcome to {{ project_name|capfirst }}</h1>
        <p class="text-xl text-gray-600 mb-6">Your new Django project is ready to go!</p>
        <div class="flex space-x-4">
            <a href="/admin" class="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition-colors">
                Admin Panel
            </a>
            <a href="#features" class="bg-gray-200 text-gray-700 px-6 py-2 rounded-lg hover:bg-gray-300 transition-colors">
                Learn More
            </a>
        </div>
    </div>

    <!-- Features Section -->
    <div id="features" class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white rounded-lg shadow-md p-6">
            <h2 class="text-xl font-semibold text-gray-800 mb-4">Django + Tailwind</h2>
            <p class="text-gray-600">
                Modern, responsive design powered by Django and Tailwind CSS.
            </p>
        </div>
        <div class="bg-white rounded-lg shadow-md p-6">
            <h2 class="text-xl font-semibold text-gray-800 mb-4">Ready to Scale</h2>
            <p class="text-gray-600">
                Built with best practices and scalability in mind.
            </p>
        </div>
        <div class="bg-white rounded-lg shadow-md p-6">
            <h2 class="text-xl font-semibold text-gray-800 mb-4">Developer Friendly</h2>
            <p class="text-gray-600">
                Hot-reloading, clean structure, and easy to customize.
            </p>
        </div>
    </div>

    <!-- CTA Section -->
    <div class="bg-blue-50 rounded-lg shadow-md p-8 text-center">
        <h2 class="text-2xl font-bold text-gray-800 mb-4">Start Building Today</h2>
        <p class="text-gray-600 mb-6">
            Everything you need to create your next amazing project.
        </p>
        <div class="space-x-4">
            <a href="https://docs.djangoproject.com/" class="text-blue-500 hover:text-blue-600 transition-colors">
                Django Docs
            </a>
            <span class="text-gray-400">|</span>
            <a href="https://tailwindcss.com/docs" class="text-blue-500 hover:text-blue-600 transition-colors">
                Tailwind Docs
            </a>
        </div>
    </div>
</div>
{% endblock %}'''

    def _get_index_template(self, app_name):
        """Generate index.html template for regular apps."""
        return '''{% extends "base.html" %}

{% block title %}{{ app_name|capfirst }} Home{% endblock %}

{% block content %}
<div class="bg-white shadow-md rounded-lg p-6">
    <h1 class="text-3xl font-bold text-gray-800 mb-4">{{ app_name|capfirst }}</h1>

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
        """Generate about.html template."""
        return '''{% extends "base.html" %}

{% block title %}About {{ app_name|capfirst }}{% endblock %}

{% block content %}
<div class="bg-white shadow-md rounded-lg p-6">
    <h1 class="text-3xl font-bold text-gray-800 mb-4">About {{ app_name|capfirst }}</h1>

    <div class="space-y-6">
        <div class="bg-gray-50 p-4 rounded-lg">
            <h2 class="text-xl font-semibold text-gray-800 mb-2">Our Mission</h2>
            <p class="text-gray-600">
                This is a sample about page for the {{ app_name }} application.
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
            </div>
        </div>
    </div>
</div>
{% endblock %}'''