from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path
from django.views import debug


urlpatterns = [
    path("admin/", admin.site.urls),
    # This will serve the built-in welcome template at /
    path("", debug.default_urlconf),  # shows Django's welcome page in DEBUG mode
] + debug_toolbar_urls()
