import unittest


from django.test import TestCase


# Create your tests here.
from faker import Faker

from racemate.models import MyUser


class LoginTestCase(unittest.TestCase):
    def setUp(self):
        """Populate test database with random data."""
        self.faker = Faker("pl_PL")
        for _ in range(5):
            MyUser.objects.create(username=self.faker.name())

