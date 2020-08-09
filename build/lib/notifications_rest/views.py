from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.generics import CreateAPIView
from .serializers import NotificationSerializer
from notifications.models import Notification


class UnreadNotificationsList(ViewSet):
    serializer_class = NotificationSerializer

    def list(self, request, *args, **kwargs):
        queryset = Notification.objects.filter(recipient_id=request.user.id, unread=True)
        return Response(NotificationSerializer(queryset, many=True).data)


class MarkAllAsRead(APIView):
    serializer_class = NotificationSerializer

    def get(self, request, format=None):
        queryset = Notification.objects.filter(recipient_id=request.user.id, unread=True)
        queryset.update(unread=False)
        return Response({'code': 'OK'}, status=status.HTTP_200_OK)


class MarkAsRead(APIView):
    serializer_class = NotificationSerializer

    def get(self, request, *args, **kwargs):
        notification_id = kwargs.get('slug')
        notification_obj = Notification.objects.get(id=notification_id)
        notification_obj.unread = False
        notification_obj.save()
        return Response({'code': 'OK'}, status=status.HTTP_200_OK)


class MarkAsUnread(APIView):
    serializer_class = NotificationSerializer

    def get(self, request, *args, **kwargs):
        notification_id = kwargs.get('slug')
        notification_obj = Notification.objects.get(id=notification_id)
        notification_obj.unread = True
        notification_obj.save()
        return Response({'code': 'OK'}, status=status.HTTP_200_OK)


class Delete(APIView):
    serializer_class = NotificationSerializer

    def delete(self, request, *args, **kwargs):
        notification_id = kwargs.get('slug')
        notification_obj = Notification.objects.get(id=notification_id)
        notification_obj.delete()
        return Response({'code': 'OK'}, status=status.HTTP_200_OK)


class AddNotification(CreateAPIView):
    serializer_class = NotificationSerializer

    def create(self, request, *args, **kwargs):
        response = super(AddNotification, self).create(request, *args, **kwargs)
        return response


class AllNotification(ViewSet):
    serializer_class = NotificationSerializer

    def list(self, request, *args, **kwargs):
        queryset = Notification.objects.filter(recipient_id=request.user.id)
        return Response(NotificationSerializer(queryset, many=True).data)


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
