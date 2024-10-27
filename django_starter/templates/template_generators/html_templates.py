"""HTML template generator for Django apps."""

def get_main_index_template():
    """Generate index.html template for main app."""
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

def get_index_template(app_name):
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

def get_about_template(app_name):
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