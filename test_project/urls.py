from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path(
        "notifications/", include("notifications_rest.urls"), name="notifications_rest"
    ),
    path("admin/", admin.site.urls),
]
