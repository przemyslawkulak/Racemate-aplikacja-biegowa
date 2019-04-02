from django.test import TestCase, Client

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from racemate.models import MyUser


class TestMyUserViewSet(APITestCase):
    """
    TestCase for MyUserViewSet
    """

    def setUp(self):
        self.client = Client()

        self.credentials = {
            'username': 'testuser',
            'password': 'testpassword'}
        self.user = MyUser.objects.create_user(**self.credentials)

    def test_correct_list_url(self):
        """
        Test for correct list url(forbidden when user is not logged)
        """
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.login(**self.credentials)
        response = self.client.get("/api/v1/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_correct_url(self):
        """
        Test for correct url for user details
        """
        self.client.login(**self.credentials)
        response = self.client.get(f"/api/v1/users/1")
        self.assertEqual(response.status_code, status.HTTP_301_MOVED_PERMANENTLY)

    def test_create_user(self):
        """
        Test for POST - method not allowed (forbidden when user is not logged)
        """
        response = self.client.post("/api/v1/users/", {'username': 'newuser', 'password': 'testpassword'},
                                    content_type='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.login(**self.credentials)

        response = self.client.post("/api/v1/users/", {'username': 'newuser', 'password': 'testpassword'},
                                    content_type='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_user(self):
        """
        Test for Put - method not allowed (forbidden when user is not logged)
        """
        response = self.client.put("/api/v1/users/", {'username': 'newuser2', 'password': 'testpassword'},
                                   content_type='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.login(**self.credentials)
        response = self.client.put("/api/v1/users/", {'username': 'newuser2', 'password': 'testpassword'},
                                   content_type='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_patch_user(self):
        """
        Test for Patch - method not allowed (forbidden when user is not logged)
        """
        response = self.client.patch("/api/v1/users/", {'username': 'newuser2', 'password': 'testpassword'},
                                     content_type='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.login(**self.credentials)
        response = self.client.patch("/api/v1/users/", {'username': 'newuser2', 'password': 'testpassword'},
                                     content_type='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_user(self):
        """
        Test for Delete - method not allowed (forbidden when user is not logged)
        """
        user = MyUser.objects.get(username='testuser')
        response = self.client.delete("/api/v1/users/", user, content_type='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.login(**self.credentials)
        response = self.client.delete("/api/v1/users/", user, content_type='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def tearDown(self):
        MyUser.objects.filter(username='user').delete()
