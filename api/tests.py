from django.test import Client

# Create your tests here.

from rest_framework import status
from rest_framework.test import APITestCase
from racemate.models import MyUser, RunningGroup, PastTraining


#
# class TestMyUserViewSet(APITestCase):
#     """
#     TestCase for MyUserViewSet
#     """
#
#     def setUp(self):
#         self.client = Client()
#
#         self.credentials = {
#             'username': 'testuser',
#             'password': 'testpassword'}
#         self.user = MyUser.objects.create_user(**self.credentials)
#
#     def test_correct_list_url(self):
#         """
#         Test for correct list url(forbidden when user is not logged)
#         """
#         response = self.client.get("/api/v1/users/")
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.client.login(**self.credentials)
#         response = self.client.get("/api/v1/users/")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_correct_url(self):
#         """
#         Test for correct url for user details
#         """
#         self.client.login(**self.credentials)
#         response = self.client.get(f"/api/v1/users/1", follow=True)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_create_user(self):
#         """
#         Test for POST - method not allowed (forbidden when user is not logged)
#         """
#         response = self.client.post("/api/v1/users/", {'username': 'newuser', 'password': 'testpassword'},
#                                     content_type='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.client.login(**self.credentials)
#
#         response = self.client.post("/api/v1/users/", {'username': 'newuser', 'password': 'testpassword'},
#                                     content_type='json')
#         self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
#
#     def test_put_user(self):
#         """
#         Test for Put - method not allowed (forbidden when user is not logged)
#         """
#         response = self.client.put("/api/v1/users/", {'username': 'newuser2', 'password': 'testpassword'},
#                                    content_type='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.client.login(**self.credentials)
#         response = self.client.put("/api/v1/users/", {'username': 'newuser2', 'password': 'testpassword'},
#                                    content_type='json')
#         self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
#
#     def test_patch_user(self):
#         """
#         Test for Patch - method not allowed (forbidden when user is not logged)
#         """
#         response = self.client.patch("/api/v1/users/", {'username': 'newuser2', 'password': 'testpassword'},
#                                      content_type='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.client.login(**self.credentials)
#         response = self.client.patch("/api/v1/users/", {'username': 'newuser2', 'password': 'testpassword'},
#                                      content_type='json')
#         self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
#
#     def test_delete_user(self):
#         """
#         Test for Delete - method not allowed (forbidden when user is not logged)
#         """
#         user = MyUser.objects.get(username='testuser')
#         response = self.client.delete("/api/v1/users/", user, content_type='json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#         self.client.login(**self.credentials)
#         response = self.client.delete("/api/v1/users/", user, content_type='json')
#         self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
#
#     def tearDown(self):
#         MyUser.objects.filter(username='user').delete()
#
#
# class TestRunningGroupViewSet(APITestCase):
#     """
#     TestCase for RunningGroupViewSet
#     """
#
#     def setUp(self):
#         self.client = Client()
#         self.credentials1 = {
#             'username': 'testuser',
#             'password': 'testpassword'}
#         user1 = MyUser.objects.create_user(**self.credentials1)
#
#         self.credentials2 = {
#             'username': 'testuser2',
#             'password': 'testpassword'}
#         user2 = MyUser.objects.create_user(**self.credentials2)
#
#         self.credentials3 = {
#             'name': 'testgroup'}
#         group = RunningGroup.objects.create(**self.credentials3)
#         group.admins.add(MyUser.objects.get(username='testuser'))
#
#     def test_correct_list_url(self):
#         """
#         Test for correct list url
#         """
#         self.client.login(**self.credentials1)
#         response = self.client.get("/api/v1/groups/")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_correct_url(self):
#         """
#         Test for correct url for group details
#         """
#         self.client.login(**self.credentials1)
#         group_id = RunningGroup.objects.get(name='testgroup').id
#
#         response = self.client.get(f"/api/v1/groups/{group_id}", follow=True)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#     def test_create_group(self):
#         """
#         Test for POST - method allowed 201_CREATED
#         """
#         response = self.client.post("/api/v1/groups/", {'name': 'testgroup'})
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#     def test_put_group(self):
#         """
#         Test for Put - method allowed (forbidden when user is not an admin)
#         """
#
#         # unlogged user
#
#         group_id = RunningGroup.objects.first().id
#         response = self.client.put(f"/api/v1/groups/{group_id}/",
#                                    {'name': 'testgroup1', 'members': [], 'admins': []})
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#         # logged admin
#
#         self.client.login(**self.credentials1)
#         group_id = RunningGroup.objects.first().id
#         response = self.client.put(f"/api/v1/groups/{group_id}/",
#                                    {'name': 'testgroup1', 'members': [], 'admins': []},
#                                    content_type='application/json', follow=True)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         # logged not an admin
#
#         self.client.login(**self.credentials2)
#         group_id = RunningGroup.objects.first().id
#         response = self.client.put(f"/api/v1/groups/{group_id}/",
#                                    {'name': 'testgroup1', 'members': [], 'admins': []},
#                                    content_type='application/json', follow=True)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_patch_group(self):
#         """
#         Test for Patch - method allowed (forbidden when user is not an admin)
#         """
#
#         # unlogged user
#
#         group_id = RunningGroup.objects.first().id
#         response = self.client.patch(f"/api/v1/groups/{group_id}/", {'name': 'testgroup1'},
#                                      content_type='application/json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#         # logged admin
#
#         self.client.login(**self.credentials1)
#         group_id = RunningGroup.objects.first().id
#         response = self.client.patch(f"/api/v1/groups/{group_id}/", {'name': 'testgroup1'},
#                                      content_type='application/json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#
#         # logged not an admin
#
#         self.client.login(**self.credentials2)
#         group_id = RunningGroup.objects.first().id
#         response = self.client.patch(f"/api/v1/groups/{group_id}/", {'name': 'testgroup1'},
#                                      content_type='application/json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#     def test_delete_group(self):
#         """
#         Test for Delete - method allowed (forbidden when user is not an admin)
#         """
#
#         # unlogged user
#
#         group_id = RunningGroup.objects.get(name='testgroup').id
#         response = self.client.delete(f"/api/v1/groups/{group_id}/", content_type='application/json',
#                                       follow=True)
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#         # logged admin
#
#         self.client.login(**self.credentials2)
#         response = self.client.delete(f"/api/v1/groups/{group_id}/", content_type='application/json')
#         self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
#
#         # logged not an admin
#
#         group_id = RunningGroup.objects.get(name='testgroup').id
#         self.client.login(**self.credentials1)
#         response = self.client.delete(f"/api/v1/groups/{group_id}/", content_type='application/json')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#
#     def tearDown(self):
#         RunningGroup.objects.filter(name='testgroup').delete()


class TestPastTrainingViewSet(APITestCase):
    """
    TestCase for PastTrainingViewSet
    """

    def setUp(self):
        self.client = Client()
        self.credentials1 = {
            'username': 'testuser',
            'password': 'testpassword'}
        self.user1 = MyUser.objects.create_user(**self.credentials1)

        self.credentials2 = {
            'username': 'testuser2',
            'password': 'testpassword'}
        user2 = MyUser.objects.create_user(**self.credentials2)

        self.credentials3 = {
            'name': 'test_training',
            'time_total': 3610,
            'distance_total': 9700,
            'date': '2019-04-01 12:12',
            'user': self.user1
        }
        pasttraining = PastTraining.objects.create(**self.credentials3)

    def test_correct_list_url(self):
        """
        Test for correct list url
        """
        self.client.login(**self.credentials1)
        response = self.client.get("/api/v1/pasttrainings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_correct_url(self):
        """
        Test for correct url for past training details
        """
        self.client.login(**self.credentials1)
        pasttrainings_id = PastTraining.objects.get(name='test_training').id
        response = self.client.get(f"/api/v1/pasttrainings/{pasttrainings_id}", follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_group(self):
        """
        Test for POST - method allowed 201_CREATED
        """

        user_id = MyUser.objects.first().id
        response = self.client.post("/api/v1/pasttrainings/",
                                    {'name': 'test_training', 'time_total_in_sec': 3610, 'distance_total_in_m': 9700,
                                     'date': '2019-04-01 12:12',
                                     'user': f'http://localhost:8000/api/v1/users/{user_id}/'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_past_training(self):
        """
        Test for Put - method allowed (not found when user is not an admin)
        """

        # logged admin

        self.client.login(**self.credentials1)
        pasttrainings_id = PastTraining.objects.first().id
        user_id = MyUser.objects.first().id
        response = self.client.put(f"/api/v1/pasttrainings/{pasttrainings_id}/",
                                   {'name': 'test_training1', 'time_total_in_sec': 3610, 'distance_total_in_m': 9700,
                                    'date': '2019-04-01 12:12',
                                    'user': f'http://localhost:8000/api/v1/users/{user_id}/'},
                                   content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # logged not an admin

        self.client.login(**self.credentials2)
        pasttrainings_id = PastTraining.objects.first().id
        user_id = MyUser.objects.first().id
        response = self.client.put(f"/api/v1/pasttrainings/{pasttrainings_id}/",
                                   {'name': 'test_training1', 'time_total_in_sec': 3610, 'distance_total_in_m': 9700,
                                    'date': '2019-04-01 12:12',
                                    'user': f'http://localhost:8000/api/v1/users/{user_id}/'},
                                   content_type='application/json', follow=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_past_training(self):
        """
        Test for Patch - method allowed (not found when user is not an admin)
        """

        # logged admin

        self.client.login(**self.credentials1)
        pasttrainings_id = PastTraining.objects.first().id
        response = self.client.patch(f"/api/v1/pasttrainings/{pasttrainings_id}/", {'name': 'test_training1'},
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # logged not an admin

        self.client.login(**self.credentials2)
        pasttrainings_id = PastTraining.objects.first().id
        response = self.client.patch(f"/api/v1/pasttrainings/{pasttrainings_id}/", {'name': 'test_training1'},
                                     content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # def test_delete_past_training(self):
    #     """
    #     Test for Delete - method allowed (forbidden when user is not an admin)
    #     """
    #
    #     # unlogged user
    #
    #     group_id = RunningGroup.objects.get(name='testgroup').id
    #     response = self.client.delete(f"/api/v1/groups/{group_id}/", content_type='application/json',
    #                                   follow=True)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #
    #     # logged admin
    #
    #     self.client.login(**self.credentials2)
    #     response = self.client.delete(f"/api/v1/groups/{group_id}/", content_type='application/json')
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #
    #     # logged not an admin
    #
    #     group_id = RunningGroup.objects.get(name='testgroup').id
    #     self.client.login(**self.credentials1)
    #     response = self.client.delete(f"/api/v1/groups/{group_id}/", content_type='application/json')
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def tearDown(self):
        RunningGroup.objects.filter(name='testgroup').delete()
