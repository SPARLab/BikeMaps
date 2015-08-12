from django.test import TestCase

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your tests here.
class TestUserFunction(TestCase):
    """Test getting various urls for user app"""
    def setUp(self):
        self.test_user = create_user()

    def test_getting_login(self):
        self.assertEqual(self.client.get('/user/login/').status_code, 200)

    def test_getting_register(self):
        self.assertEqual(self.client.get('/user/register/').status_code, 200)

    def test_login(self):
        self.assertFalse(self.client.login(username="test_user", password="wrong_password"))
        self.assertFalse(self.client.login(username="nonexistant_user", password="password"))
        self.assertTrue(self.client.login(username="test_user", password="password"))

def create_user():
    return User.objects.create_user("test_user", email="user@bikemaps.org", password="password")

def create_superuser():
    return User.objects.create_superuser("test_superuser", email="super_user@bikemaps.org", password="password")
