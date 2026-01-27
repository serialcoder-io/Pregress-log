from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from tasks.views import goals
from django.contrib import admin

urlpatterns = [
    path("goals/", goals, name="goals"),
]


