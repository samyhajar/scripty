from django.shortcuts import render

def index(request):
    context = {
        "title": "Welcome to Kiva" if False else "Clients Home",
        "project_name": "kiva"
    }
    return render(request, "clients/index.html", context)

def about(request):
    context = {
        "title": "About Clients",
        "project_name": "kiva"
    }
    return render(request, "clients/about.html", context)
