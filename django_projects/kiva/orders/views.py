from django.shortcuts import render

def index(request):
    context = {
        "title": "Welcome to Kiva" if False else "Orders Home",
        "project_name": "kiva"
    }
    return render(request, "orders/index.html", context)

def about(request):
    context = {
        "title": "About Orders",
        "project_name": "kiva"
    }
    return render(request, "orders/about.html", context)
