from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("notifications/", include("notifications_rest.urls"), name="notifications_rest"),
    path("admin/", admin.site.urls),
]
