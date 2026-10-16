from django.urls import include, path

from notifications_rest.urls import router

urlpatterns = [
    path("viewset/", include(router.urls)),
]
