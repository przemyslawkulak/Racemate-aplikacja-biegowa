# Create your tests here.
from unittest import TestCase
from django.test import Client

from racemate.forms import LoginForm
from racemate.models import MyUser


class User_Form_Test(TestCase):

    # Valid Form Data
    def test_UserForm_valid(self):
        form = LoginForm(data={'login': "testuser", 'password': "testpsswrd"})
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_UserForm_invalid(self):
        form = LoginForm(data={'login': "", 'password': "mp", })
        self.assertFalse(form.is_valid())


class LoginTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.credentials = {
            'username': 'user',
            'password': 'testpsswrd'}
        self.user = MyUser.objects.create_user(**self.credentials)

    def test_correct_login(self):
        # Get login page
        response = self.client.get('/accounts/login/')

        # Check response code
        self.assertEquals(response.status_code, 200)

        # Log the user in
        self.client.login(**self.credentials)

        # Check response code
        response = self.client.get('/accounts/login/')
        self.assertEquals(response.status_code, 200)
        print(response.context['user'].username)

        # check if user is correct for credentials
        self.assertEquals(response.context['user'].username, 'user')

        # check if user is not anonymous
        self.assertFalse(self.user.is_anonymous)

        response = self.client.get('/logout/')

        self.assertIsNone(response.context)

    def test_incorrect_login(self):
        self.credentials = {
            'username': 'user2',
            'password': 'testpsswrd'}

        # Log the incorect user in
        self.client.login(**self.credentials)

        response = self.client.get('/accounts/login/')
        print(response.context)
        # check if uer from cresentials is not logged
        self.assertNotEquals(response.context['user'].username, 'user2')


    def tearDown(self):
        MyUser.objects.filter(username='user').delete()


class LogoutTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.credentials = {
            'username': 'user',
            'password': 'testpsswrd'}
        self.user = MyUser.objects.create(**self.credentials)

    def test_logout(self):
        # Log out
        response = self.client.get('/logout/')
        # check response code
        self.assertEquals(response.status_code, 302)


    def tearDown(self):
        MyUser.objects.filter(username='user').delete()
