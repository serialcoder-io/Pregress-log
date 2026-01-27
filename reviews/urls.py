from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from reviews.views import reviews_view
from django.contrib import admin

urlpatterns = [
    path("", reviews_view, name="reviews"),
]

