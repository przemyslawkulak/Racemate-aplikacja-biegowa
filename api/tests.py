from django.test import Client

# Create your tests here.

from rest_framework import status
from rest_framework.test import APITestCase
from racemate.models import MyUser, RunningGroup


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
        response = self.client.get(f"/api/v1/users/1", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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


class RunningGroupViewSet(APITestCase):
    """
    TestCase for MyUserViewSet
    """

    def setUp(self):
        self.client = Client()
        self.credentials1 = {
            'username': 'testuser',
            'password': 'testpassword'}
        user1 = MyUser.objects.create_user(**self.credentials1)

        self.credentials2 = {
            'username': 'testuser2',
            'password': 'testpassword'}
        user2 = MyUser.objects.create_user(**self.credentials2)

        self.credentials3 = {
            'name': 'testgroup'}
        group = RunningGroup.objects.create(**self.credentials3)
        group.admins.add(MyUser.objects.get(username='testuser'))

    def test_correct_list_url(self):
        """
        Test for correct list url
        """
        self.client.login(**self.credentials1)
        response = self.client.get("/api/v1/groups/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_correct_url(self):
        """
        Test for correct url for user details
        """
        self.client.login(**self.credentials1)
        group_id = RunningGroup.objects.get(name='testgroup').id

        response = self.client.get(f"/api/v1/groups/{group_id}", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        """
        Test for POST - method allowed 201_CREATED
        """
        response = self.client.post("/api/v1/groups/", {'name': 'testgroup'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_user(self):
        """
        Test for Put - method allowed (not allowed when user is not logged)
        """
        group_id = RunningGroup.objects.first().id
        response = self.client.put(f"/api/v1/groups/{group_id}/",
                                   {'name': 'testgroup1', 'members': [], 'admins': []})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.login(**self.credentials1)
        group_id = RunningGroup.objects.first().id
        response = self.client.put(f"/api/v1/groups/{group_id}/",
                                   {'name': 'testgroup1', 'members': [], 'admins': []},
                                   content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_patch_user(self):
        """
        Test for Patch - method allowed (forbidden when user is not logged)
        """
        group_id = RunningGroup.objects.first().id
        response = self.client.patch(f"/api/v1/groups/{group_id}/", {'name': 'testgroup1'},
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.login(**self.credentials1)
        group_id = RunningGroup.objects.first().id
        response = self.client.patch(f"/api/v1/groups/{group_id}/", {'name': 'testgroup1'},
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        """
        Test for Delete - method allowed (forbidden when user is not logged)
        """
        group = RunningGroup.objects.first()
        group_id = RunningGroup.objects.first().id
        response = self.client.delete(f"/api/v1/groups/{group_id}/", group, content_type='application/json',
                                      follow=True)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.login(**self.credentials1)
        response = self.client.delete(f"/api/v1/groups/{group_id}/", content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
