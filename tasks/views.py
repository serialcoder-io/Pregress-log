from django.shortcuts import render

def goals(request):
    if request.htmx:
        return render(request, "cotton/partials/goals_partial.html")
    return render(request, "tasks/goals.html")