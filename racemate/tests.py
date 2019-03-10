# Create your tests here.
from unittest import TestCase
from django.test import Client

from racemate.forms import LoginForm
from racemate.models import MyUser


class LoginTestCase(TestCase):

    def setUp(self):
        self.client = Client()

        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        self.user = MyUser.objects.create(**self.credentials)

    def test_login(self):
        # Get login page
        response = self.client.get('/accounts/login/')

        # Check response code
        self.assertEquals(response.status_code, 200)

        # Log the user in
        self.client.login(username='XXX', password="XXX")

        # Check response code
        response = self.client.get('/accounts/login/')
        self.assertEquals(response.status_code, 200)

        self.assertTrue(self.user.is_authenticated)

    def test_logout(self):
        # Log in
        self.client.login(username='XXX', password="XXX")

    def tearDown(self):
        self.credentials = {
            'username': 'testuser',
            'password': 'secret'}
        MyUser.objects.filter(**self.credentials).delete()


class User_Form_Test(TestCase):

    # Valid Form Data
    def test_UserForm_valid(self):
        form = LoginForm(data={'login': "user3", 'password': "user"})
        self.assertTrue(form.is_valid())

    # Invalid Form Data
    def test_UserForm_invalid(self):
        form = LoginForm(data={'email': "", 'password': "mp", })
        self.assertFalse(form.is_valid())
