from django.conf.urls.i18n import i18n_patterns
from django.urls import path
from users.views import dashboard
from django.contrib import admin

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
]

