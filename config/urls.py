from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from config import settings
from users.views import index
from django.contrib import admin
from debug_toolbar.toolbar import debug_toolbar_urls

"""urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),  # switcher de langue
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("", include("users.urls")),
    path("tasks", include("tasks.urls")),
    path("reviews", include("reviews.urls")),
    path("", index, name="home"),
)"""

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("account/", include("users.urls")),
    path("tasks/", include("tasks.urls")),
    path("reviews/", include("reviews.urls")),
    path("", index, name="home"),
] 

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
