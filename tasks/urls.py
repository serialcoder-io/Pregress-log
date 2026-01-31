from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from tasks.views import goals, goal_details, subgoal_details
from django.contrib import admin

urlpatterns = [
    path("", goals, name="goals"),
    path("<uuid:goal_id>/", goal_details, name="goal_details"),
    path("<uuid:goal_id>/subgoals/<uuid:subgoal_id>/", subgoal_details, name="subgoal_details"),
]


