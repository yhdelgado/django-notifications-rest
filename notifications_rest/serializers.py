from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType

from notifications.models import Notification

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

UserModel = get_user_model()


class UserSerializer(ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = UserModel
        fields = ['id']


class GenericSerializer(Serializer):
    pk = serializers.SerializerMethodField()
    content_type_name = serializers.SerializerMethodField()
    content_type_model = serializers.SerializerMethodField()
    content_type_app = serializers.SerializerMethodField()
    content_type_id = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    string = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'

    def get_pk(self, obj):
        return obj.pk

    def get_obj_content_type(self, obj):
        if not hasattr(self, 'obj_content_type'):
            self.obj_content_type = ContentType.objects.get_for_model(obj)
        return self.obj_content_type

    def get_content_type_app(self, obj):
        return self.get_obj_content_type(obj).app_label

    def get_content_type_model(self, obj):
        return self.get_obj_content_type(obj).model

    def get_content_type_name(self, obj):
        return self.get_obj_content_type(obj).name

    def get_content_type_id(self, obj):
        return self.get_obj_content_type(obj).id

    def get_string(self, obj):
        return obj.__str__()

    def get_url(self, obj):
        try:
            return obj.get_absolute_url()
        except AttributeError:
            return ''


class NotificationSerializer(ModelSerializer):
    recipient = UserSerializer()
    actor = GenericSerializer()
    verb = serializers.CharField()
    level = serializers.CharField()
    description = serializers.CharField()
    timestamp = serializers.DateTimeField(read_only=True)
    unread = serializers.BooleanField()
    public = serializers.BooleanField()
    deleted = serializers.BooleanField()
    emailed = serializers.BooleanField()
    target = GenericSerializer()
    action_object = GenericSerializer()
    string = serializers.CharField(source="__str__")

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'target', 'verb', 'action_object', 'level',
                  'description', 'unread', 'public', 'deleted',
                  'emailed', 'timestamp', 'string']

    def create(self, validated_data):
        recipient_data = validated_data.pop('recipient')
        recipient = UserModel.objects.get_or_create(id=recipient_data['id'])
        actor_data = validated_data.pop('actor')
        actor = UserModel.objects.get_or_create(id=actor_data['id'])
        notification = Notification.objects.create(recipient=recipient[0], actor=actor[0], **validated_data)
        return notification
