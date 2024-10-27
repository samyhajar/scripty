from django.shortcuts import render

def index(request):
    context = {
        "title": "Welcome to Kiva" if True else "Home Home",
        "project_name": "kiva"
    }
    return render(request, "home/index.html", context)

def about(request):
    context = {
        "title": "About Home",
        "project_name": "kiva"
    }
    return render(request, "home/about.html", context)
