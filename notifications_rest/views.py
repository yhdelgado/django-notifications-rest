from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.generics import CreateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from .serializers import NotificationSerializer
from notifications.models import Notification


class UnreadNotificationsList(ListModelMixin, GenericViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self, *args, **kwargs):
        return Notification.objects.filter(recipient_id=self.request.user.id, unread=True)


class MarkAllAsRead(APIView):
    serializer_class = NotificationSerializer

    def get(self, request, format=None):
        queryset = Notification.objects.filter(recipient_id=request.user.id, unread=True)
        queryset.update(unread=False)
        return Response({'code': 'OK'}, status=status.HTTP_200_OK)


class NotificationMixin:
    def get_obj(self, request, *args, **kwargs):
        notification_id = kwargs.get('slug')
        queryset = Notification.objects.filter(recipient=request.user)
        return queryset.get(id=notification_id)


class MarkAsRead(NotificationMixin, APIView):
    serializer_class = NotificationSerializer

    def get(self, request, *args, **kwargs):
        notification_obj = self.get_obj(request, *args, **kwargs)
        notification_obj.unread = False
        notification_obj.save()
        return Response({'code': 'OK'}, status=status.HTTP_200_OK)


class MarkAsUnread(NotificationMixin, APIView):
    serializer_class = NotificationSerializer

    def get(self, request, *args, **kwargs):
        notification_obj = self.get_obj(request, *args, **kwargs)
        notification_obj.unread = True
        notification_obj.save()
        return Response({'code': 'OK'}, status=status.HTTP_200_OK)


class Delete(NotificationMixin, APIView):
    serializer_class = NotificationSerializer

    def delete(self, request, *args, **kwargs):
        notification_obj = self.get_obj(request, *args, **kwargs)
        notification_obj.delete()
        return Response({'code': 'OK'}, status=status.HTTP_200_OK)


class AddNotification(CreateAPIView):
    serializer_class = NotificationSerializer

    def create(self, request, *args, **kwargs):
        response = super(AddNotification, self).create(request, *args, **kwargs)
        return response


class AllNotification(ListModelMixin, GenericViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self, *args, **kwargs):
        return Notification.objects.filter(recipient_id=self.request.user.id)


class UnreadNotificationCount(APIView):
    serializer_class = NotificationSerializer

    def get(self, request, *args, **kwargs):
        queryset = Notification.objects.filter(recipient_id=request.user.id, unread=True)
        count = queryset.count()
        data = {
            'unread_count': count
        }
        return Response(data)


class AllNotificationCount(APIView):
    serializer_class = NotificationSerializer

    def get(self, request, *args, **kwargs):
        queryset = Notification.objects.filter(recipient_id=request.user.id)
        count = queryset.count()
        data = {
            'all_count': count
        }
        return Response(data)


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
