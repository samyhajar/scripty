"""URL template generator for Django apps."""

def get_urls_template(app_name):
    """Generate urls.py content for the app."""
    return f'''from django.urls import path
from . import views

app_name = "{app_name}"

urlpatterns = [
    path("", views.index, name="index"),
    path("about/", views.about, name="about"),
]
'''