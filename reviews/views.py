from django.shortcuts import render

def reviews_view(request):
    return render(request, "reviews/reviews.html")