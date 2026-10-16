from django.contrib.auth import get_permission_codename, get_user_model
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError as DjangoValidationError
from notifications.models import Notification
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, Serializer

UserModel = get_user_model()


class UserSerializer(ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = UserModel
        fields = ["id"]


class ObjectReferenceSerializer(Serializer):
    content_type_id = serializers.PrimaryKeyRelatedField(queryset=ContentType.objects.all())
    pk = serializers.CharField()


class GenericSerializer(Serializer):
    default_error_messages = {
        "no_object": "No object that you may view has this content_type_id and pk.",
    }

    pk = serializers.SerializerMethodField()
    content_type_name = serializers.SerializerMethodField(read_only=True)
    content_type_model = serializers.SerializerMethodField(read_only=True)
    content_type_app = serializers.SerializerMethodField(read_only=True)
    content_type_id = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField(read_only=True)
    string = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = "__all__"

    def get_obj(self, data):
        reference = ObjectReferenceSerializer(data=data)
        reference.is_valid(raise_exception=True)
        model_class = reference.validated_data["content_type_id"].model_class()
        if model_class is None:
            self.fail("no_object")
        try:
            pk = model_class._meta.pk.to_python(reference.validated_data["pk"])
        except DjangoValidationError:
            self.fail("no_object")
        obj = model_class._default_manager.filter(pk=pk).first()
        if obj is None or not self.may_reference(obj):
            self.fail("no_object")
        return obj

    def may_reference(self, obj):
        user = self.context["request"].user
        view_permission = f"{obj._meta.app_label}.{get_permission_codename('view', obj._meta)}"
        return obj == user or user.has_perm(view_permission)

    def to_internal_value(self, data):
        return self.get_obj(data)

    def get_pk(self, obj):
        return obj.pk

    def get_obj_content_type(self, obj):
        return ContentType.objects.get_for_model(obj)

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
            return ""


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
    target = GenericSerializer(required=False)
    action_object = GenericSerializer(required=False)
    string = serializers.CharField(source="__str__", read_only=True)

    class Meta:
        model = Notification
        fields = [
            "id",
            "recipient",
            "actor",
            "target",
            "verb",
            "action_object",
            "level",
            "description",
            "unread",
            "public",
            "deleted",
            "emailed",
            "timestamp",
            "string",
        ]

    def validate_recipient(self, value):
        recipient = UserModel._default_manager.filter(id=value["id"]).first()
        if recipient is None:
            raise ValidationError("No user has this id.")
        return recipient

    def create(self, validated_data):
        return Notification.objects.create(**validated_data)
