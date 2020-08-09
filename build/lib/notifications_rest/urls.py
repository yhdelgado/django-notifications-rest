from django.urls import re_path as url
from .views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register('', NotificationViewSet)

app_name = 'notifications_rest'
urlpatterns = [
    url(r'^add/', AddNotification.as_view(), name='add'),
    url(r'^all/', AllNotification.as_view({'get': 'list'}), name='all'),
    url(r'^unread/', UnreadNotificationsList.as_view({'get': 'list'}), name='unread'),
    url(r'^mark-all-as-read/$', MarkAllAsRead.as_view(), name='mark_all_as_read'),
    url(r'^mark-as-read/(?P<slug>\d+)/$', MarkAsRead.as_view(), name='mark_as_read'),
    url(r'^mark-as-unread/(?P<slug>\d+)/$', MarkAsUnread.as_view(), name='mark_as_unread'),
    url(r'^delete/(?P<slug>\d+)/$', Delete.as_view(), name='delete'),
    url(r'^api/unread_count/$', UnreadNotificationCount.as_view(), name='live_unread_notification_count'),
    url(r'^api/all_count/$', AllNotificationCount.as_view(), name='live_all_notification_count'),
    url(r'^api/unread_list/$', UnreadNotificationsList.as_view({'get': 'list'}), name='live_unread_notification_list'),
]
