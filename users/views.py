from django.shortcuts import render

def index(request):
    return render(request, "index.html")

def dashboard(request):
    if request.htmx:
        print("htmx request")
        return render(request, "cotton/partials/dashboard_partial.html")
    return render(request, "users/dashboard.html")