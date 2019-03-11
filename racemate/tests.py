# Create your tests here.
import string
from random import random, randint, choice
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
        # check if user from cresentials is not logged
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


#################################################################################################################
# RegisterView tests

class RegisterTestCase(TestCase):

    def _generator_string(self, size,
                          chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
        return ''.join(choice(chars) for _ in range(size))

    def _generator_username(self):
        size = randint(5, 20)
        return self._generator_string(size)

    def _generator_password(self):
        size = randint(5, 20)
        return self._generator_string(size)

    def _generator_email(self):
        size = randint(5, 20)
        size2 = randint(1, 5)
        return self._generator_string(size) + '@' + self._generator_string(size2) + '.' + self._generator_string(
            size2)

    def setUp(self):
        self.client = Client()
        self.user = MyUser.objects.create_user(username=self._generator_username(), password=self._generator_password(),
                                               email=self._generator_email())

    def test_response_register_page(self):
        response = self.client.get('/register/')
        self.assertEquals(response.status_code, 200)

    def test_saving_user(self):
        password = self._generator_username()
        response = self.client.post('/register/',
                                    {'username': self._generator_username(), 'password': password,
                                     "email": self._generator_email(),
                                     'confirmPassword': password})

        # check proper redirect url
        self.assertEqual(response.url, "/accounts/login/")

    def test_same_username(self):
        user = MyUser.objects.all().first()
        password = self._generator_username()
        response = self.client.post('/register/',
                                    {'username': user.username, 'password': password,
                                     "email": self._generator_email(),
                                     'confirmPassword': password})
        self.assertEqual(response.context['text'], 'Username exists')

    def test_wrong_password_confirm(self):
        password = self._generator_username()
        password_confirm = password + '1'
        response = self.client.post('/register/',
                                    {'username': self._generator_username(), 'password': password,
                                     "email": self._generator_email(),
                                     'confirmPassword': password_confirm})
        self.assertEqual(response.context['text'], 'The password and confirmation password do not match')

    def test_empty_username_field(self):
        password = self._generator_username()
        response = self.client.post('/register/',
                                    {'username': '', 'password': password,
                                     "email": self._generator_email(),
                                     'confirmPassword': password})
        self.assertEqual(response.context['text'], 'Fill all fields')

    def test_empty_password_field(self):
        password = self._generator_username()
        response = self.client.post('/register/',
                                    {'username': self._generator_username(), 'password': '',
                                     "email": self._generator_email(),
                                     'confirmPassword': password})
        self.assertEqual(response.context['text'], 'Fill all fields')

    def test_empty_confirmpassword_field(self):
        password = self._generator_username()
        response = self.client.post('/register/',
                                    {'username': self._generator_username(), 'password': password,
                                     "email": self._generator_email(),
                                     'confirmPassword': ''})
        self.assertEqual(response.context['text'], 'Fill all fields')

    def test_empty_email_field(self):
        password = self._generator_username()
        response = self.client.post('/register/',
                                    {'username': self._generator_username(), 'password': password,
                                     "email": '',
                                     'confirmPassword': password})
        self.assertEqual(response.context['text'], 'Fill all fields')

    def tearDown(self):
        MyUser.objects.filter(username='user').delete()
