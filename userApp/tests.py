from django.test import TestCase

# Create your tests here.
class BasicTestCase(TestCase):
    """Test getting various urls for user app"""
    def test_getting_login(self):
        self.client.get('/user/login')

    def test_getting_register(self):
        self.client.get('/user/register')

    def test_getting_(self):
        self.client.get('/alerts')
