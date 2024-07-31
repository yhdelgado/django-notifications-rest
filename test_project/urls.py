from django.urls import include, path

urlpatterns = [
    path(
        "notifications/", include("notifications_rest.urls"), name="notifications_rest"
    ),
]
