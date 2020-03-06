from unittest.mock import patch

from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from .. import models
from . import factories


class RegistrationViewTests(APITestCase):
    def test_create(self):
        data = {
            "email": "aan-allein@example.com",
            "password": "Tai'SharMalkier",
            "first_name": "al'Lan",
            "last_name": "Mandragoran",
        }
        url = reverse("users:register")
        response = self.client.post(url, data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = models.User.objects.get(email=data["email"])
        self.assertTrue(user.check_password(data["password"]))
        self.assertEqual(response.data["token"], user.auth_token.key)


class RestorePasswordTests(APITestCase):
    @patch("users.models.User.send_password_restore_email")
    def test_post(self, send_email_mock):
        user = factories.UserFactory(email="someone@example.com")
        data = {"email": user.email.upper()}
        url = reverse("users:reset-password")
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        send_email_mock.assert_called_once_with()


class RestorePasswordConfirmTests(APITestCase):
    def test_update(self):
        user = factories.UserFactory(email="someone@email.com", password="forgotten")
        data = {
            "password": "supersecret",
            "token": default_token_generator.make_token(user),
        }
        url = reverse("users:reset-password-confirm", kwargs={"user_id": str(user.pk)})
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.check_password(data["password"]))


class ChangePasswordViewTests(APITestCase):
    def test_update(self):
        user = factories.UserFactory()
        current_password = "loremipsumdolorsitamet"
        new_password = "supersecret34134#"
        user.set_password(current_password)
        self.client.force_authenticate(user)
        url = reverse("users:change-password")
        data = {
            "current_password": current_password,
            "new_password": new_password,
        }
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user.refresh_from_db()
        self.assertTrue(user.check_password(new_password))


class UserMeViewTests(APITestCase):
    def setUp(self):
        self.user = factories.UserFactory()
        self.client.force_authenticate(user=self.user)
        self.url = reverse("users:user-me")

    def test_retrieve(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update(self):
        data = {
            "email": "newmail@example.com",
        }
        self.assertNotEqual(self.user.email, data["email"])
        response = self.client.patch(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, data["email"])

    def test_destroy(self):
        password = "bolag123"
        self.user.set_password(password)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(self.url, data={"password": password})
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(models.User.DoesNotExist):
            self.user.refresh_from_db()
