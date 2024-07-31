from django.conf import settings
from django.urls import re_path as url
from rest_framework import routers

from .views import (
    AddNotification,
    AllNotification,
    AllNotificationCount,
    Delete,
    MarkAllAsRead,
    MarkAsRead,
    MarkAsUnread,
    NotificationViewSet,
    UnreadNotificationCount,
    UnreadNotificationsList,
)

router = routers.DefaultRouter()
router.register("", NotificationViewSet)

app_name = "notifications_rest"
urlpatterns = [
    url(r"^all/", AllNotification.as_view({"get": "list"}), name="all"),
    url(r"^unread/", UnreadNotificationsList.as_view({"get": "list"}), name="unread"),
    url(r"^mark-all-as-read/$", MarkAllAsRead.as_view(), name="mark_all_as_read"),
    url(r"^mark-as-read/(?P<slug>\d+)/$", MarkAsRead.as_view(), name="mark_as_read"),
    url(r"^mark-as-unread/(?P<slug>\d+)/$", MarkAsUnread.as_view(), name="mark_as_unread"),
    url(r"^delete/(?P<slug>\d+)/$", Delete.as_view(), name="delete"),
    url(r"^unread_count/$", UnreadNotificationCount.as_view(), name="unread_notification_count"),
    url(r"^all_count/$", AllNotificationCount.as_view(), name="all_notification_count"),
]

if getattr(settings, "NOTIFICATIONS_API_ALLOW_ADD", False):
    urlpatterns += [
        url(r"^add/", AddNotification.as_view(), name="add"),
    ]
