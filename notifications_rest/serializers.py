from rest_framework.serializers import ModelSerializer, RelatedField
from rest_framework import serializers
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserSerializer(ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = UserModel
        fields = ['id', ]


class ContentTypeSerializer(ModelSerializer):
    class Meta:
        model = ContentType
        fields = ['app_label', 'model']


class GenericNotificationRelatedField(RelatedField):

    def to_representation(self, value):
        if isinstance(value, UserModel):
            serializer = UserSerializer(value)
        if isinstance(value, ContentType):
            serializer = ContentTypeSerializer(value)

        return serializer.data


class NotificationSerializer(ModelSerializer):
    recipient = UserSerializer()
    actor = UserSerializer()
    verb = serializers.CharField()
    level = serializers.CharField()
    description = serializers.CharField()
    timestamp = serializers.DateTimeField(read_only=True)
    unread = serializers.BooleanField()
    public = serializers.BooleanField()
    deleted = serializers.BooleanField()
    emailed = serializers.BooleanField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'target', 'verb', 'level', 'description', 'unread', 'public', 'deleted',
                  'emailed', 'timestamp']

    def create(self, validated_data):
        recipient_data = validated_data.pop('recipient')
        recipient = UserModel.objects.get_or_create(id=recipient_data['id'])
        actor_data = validated_data.pop('actor')
        actor = UserModel.objects.get_or_create(id=actor_data['id'])
        notification = Notification.objects.create(recipient=recipient[0], actor=actor[0], **validated_data)
        return notification
