from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from notifications.models import Notification
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

User = get_user_model()


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

    def assert_actions_not_found(self, notification_id):
        for method, name in (("get", "mark_as_read"), ("get", "mark_as_unread"), ("delete", "delete")):
            with self.subTest(view=name):
                url = reverse(f"notifications_rest:{name}", kwargs={"slug": notification_id})
                response = getattr(self.client, method)(url)
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_actions_on_missing_notification_are_not_found(self):
        missing_id = self.notification.id
        self.notification.delete()
        self.assert_actions_not_found(missing_id)

    def test_actions_on_other_users_notification_are_not_found(self):
        other_user = User.objects.create_user(username="otheruser", password="testpass")
        foreign = Notification.objects.create(recipient=other_user, actor=other_user, verb="test", unread=True)
        self.assert_actions_not_found(foreign.id)
        foreign.refresh_from_db()
        self.assertTrue(foreign.unread)

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
