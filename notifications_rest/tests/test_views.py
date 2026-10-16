from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from notifications.models import Notification
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

User = get_user_model()


CONTENT_TYPE_KEYS = ("content_type_id", "content_type_app", "content_type_model", "content_type_name")


def content_type_fields(content_type):
    values = (content_type.id, content_type.app_label, content_type.model, content_type.name)
    return dict(zip(CONTENT_TYPE_KEYS, values))


def serialized_content_type(serialized_object):
    return {key: serialized_object[key] for key in CONTENT_TYPE_KEYS}


class NotificationTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client = APIClient()
        self.client.login(username="testuser", password="testpass")
        self.notification = Notification.objects.create(
            recipient=self.user,
            actor=self.user,
            verb="test",
            description="test notification",
            unread=True,
            public=False,
            deleted=False,
            emailed=False,
        )

    def test_get_unread_notifications(self):
        url = reverse("notifications_rest:unread")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_mark_all_as_read(self):
        url = reverse("notifications_rest:mark_all_as_read")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertFalse(self.notification.unread)

    def test_mark_as_read(self):
        url = reverse("notifications_rest:mark_as_read", kwargs={"slug": self.notification.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertFalse(self.notification.unread)

    def test_mark_as_unread(self):
        self.notification.unread = False
        self.notification.save()
        url = reverse("notifications_rest:mark_as_unread", kwargs={"slug": self.notification.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.unread)

    def test_delete_notification(self):
        url = reverse("notifications_rest:delete", kwargs={"slug": self.notification.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Notification.objects.filter(id=self.notification.id).exists())

    def test_add_notification_minimal(self):
        url = reverse("notifications_rest:add")
        data = {
            "recipient": {"id": self.user.id},
            "actor": {
                "pk": self.user.id,
                "content_type_id": ContentType.objects.get_for_model(self.user).id,
            },
            "verb": "new",
            "description": "new notification",
            "unread": True,
            "public": False,
            "deleted": False,
            "level": "1",
            "emailed": False,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["recipient"]["id"], self.user.id)
        self.assertEqual(Notification.objects.count(), 2)

    def test_add_notification_full(self):
        url = reverse("notifications_rest:add")
        data = {
            "recipient": {"id": self.user.id},
            "actor": {
                "pk": self.user.id,
                "content_type_id": ContentType.objects.get_for_model(self.user).id,
            },
            "verb": "new",
            "description": "new notification",
            "unread": True,
            "public": False,
            "deleted": False,
            "level": "1",
            "emailed": False,
            "target": {
                "pk": self.user.id,
                "content_type_id": ContentType.objects.get_for_model(self.user).id,
            },
            "action_object": {
                "pk": self.user.id,
                "content_type_id": ContentType.objects.get_for_model(self.user).id,
            },
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["recipient"]["id"], self.user.id)
        self.assertEqual(Notification.objects.count(), 2)

    def test_get_all_notifications(self):
        url = reverse("notifications_rest:all")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_lists_give_each_object_its_own_content_type(self):
        group = Group.objects.create(name="testgroup")
        user_type = content_type_fields(ContentType.objects.get_for_model(User))
        group_type = content_type_fields(ContentType.objects.get_for_model(Group))
        by_group = Notification.objects.create(
            recipient=self.user, actor=group, target=self.user, action_object=group, verb="mixed"
        )
        by_user = Notification.objects.create(
            recipient=self.user, actor=self.user, target=group, action_object=self.user, verb="mixed"
        )
        expected = {
            by_group.id: {"actor": group_type, "target": user_type, "action_object": group_type},
            by_user.id: {"actor": user_type, "target": group_type, "action_object": user_type},
        }
        for name in ("all", "unread"):
            with self.subTest(view=name):
                response = self.client.get(reverse(f"notifications_rest:{name}"))
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                actual = {
                    item["id"]: {field: serialized_content_type(item[field]) for field in expected[item["id"]]}
                    for item in response.data
                    if item["id"] in expected
                }
                self.assertEqual(actual, expected)

    def test_get_unread_notification_count(self):
        url = reverse("notifications_rest:unread_notification_count")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["unread_count"], 1)

    def test_get_all_notification_count(self):
        url = reverse("notifications_rest:all_notification_count")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["all_count"], 1)
