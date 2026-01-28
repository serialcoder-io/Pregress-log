from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from tasks.views import goals, goal_details
from django.contrib import admin

urlpatterns = [
    path("goals/", goals, name="goals"),
    path("goals/<uuid:id>/", goal_details, name="goal_details"),
]


