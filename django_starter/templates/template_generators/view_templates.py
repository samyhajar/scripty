"""View template generator for Django apps."""

def get_views_template(app_name, project_name, is_main_app=False):
    """Generate views.py content for the app."""
    if is_main_app:
        return f'''from django.shortcuts import render
from clients.models import Client
from orders.models import Order

def index(request):
    clients = Client.objects.all()
    orders = Order.objects.all()
    context = {{
        "title": "Welcome to {project_name.capitalize()}",
        "project_name": "{project_name}",
        "clients": clients,
        "orders": orders
    }}
    return render(request, "{app_name}/index.html", context)

def about(request):
    context = {{
        "title": "About {app_name.capitalize()}",
        "project_name": "{project_name}"
    }}
    return render(request, "{app_name}/about.html", context)
'''
    else:
        return f'''from django.shortcuts import render

def index(request):
    context = {{
        "title": "{app_name.capitalize()} Home",
        "project_name": "{project_name}"
    }}
    return render(request, "{app_name}/index.html", context)

def about(request):
    context = {{
        "title": "About {app_name.capitalize()}",
        "project_name": "{project_name}"
    }}
    return render(request, "{app_name}/about.html", context)
'''