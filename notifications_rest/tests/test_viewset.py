from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from notifications.models import Notification
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


@override_settings(ROOT_URLCONF="notifications_rest.tests.viewset_urls")
class RoutedNotificationViewSetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        other_user = User.objects.create_user(username="otheruser", password="testpass")
        self.own = Notification.objects.create(recipient=self.user, actor=self.user, verb="own")
        self.foreign = Notification.objects.create(recipient=other_user, actor=other_user, verb="foreign")
        self.client.login(username="testuser", password="testpass")

    def detail_url(self, notification):
        return reverse("notification-detail", kwargs={"pk": notification.id})

    def test_list_shows_only_own_notifications(self):
        response = self.client.get(reverse("notification-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["id"] for item in response.data], [self.own.id])

    def test_other_users_notification_is_not_found(self):
        for method in ("get", "delete"):
            with self.subTest(method=method):
                response = getattr(self.client, method)(self.detail_url(self.foreign))
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Notification.objects.filter(id=self.foreign.id).exists())

    def test_own_notification_can_be_deleted(self):
        response = self.client.delete(self.detail_url(self.own))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Notification.objects.filter(id=self.own.id).exists())

    def test_anonymous_requests_are_rejected(self):
        self.client.logout()
        for method, url in (
            ("get", reverse("notification-list")),
            ("get", self.detail_url(self.own)),
            ("delete", self.detail_url(self.own)),
        ):
            with self.subTest(method=method, url=url):
                response = getattr(self.client, method)(url)
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Notification.objects.count(), 2)
