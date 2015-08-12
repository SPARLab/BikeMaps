from django.test import TestCase

from django.contrib.auth import get_user_model
User = get_user_model()
from blogApp.models import *

import json

# Create your tests here.
class TestURLTests(TestCase):
    """Test getting various urls for blogApp"""
    def setUp(self):
        self.test_post = Post.objects.create(title="Test Title", description="This is a test post", published=False, content="some content")

    def test_getting_blog_root(self):
        self.assertEqual(self.client.get("/blog/").status_code, 200)

    def test_getting_post(self):
        self.assertEqual(self.client.get("/blog/post/test-title").status_code, 200)

    def test_short_url(self):
        self.assertEqual(self.client.get(self.test_post.get_short_url(), follow=True).status_code, 200)

class ObjectCreationTests(TestCase):
    """Test submitting various things to the blogApp views"""
    def setUp(self):
        self.test_superuser = create_superuser()
        self.test_post = Post.objects.create(title="Test Title", description="This is a test post", published=False, content="some content")

    def test_creating_post(self):
        # TODO: Test that non superusers can't edit posts
        self.client.login(username="test_superuser", password="password")
        response = self.client.post("/blog/create/", {"title": "Test Title 2", "description": "This is a test post 2", "published": False, "content": "some content"}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_blog_edit(self):
        # TODO: Test that non superusers can't edit posts
        self.client.login(username="test_superuser", password="password")
        self.assertEqual(self.client.get("/blog/edit/test-title").status_code, 200)

        response = self.client.post("/blog/edit/test-title", {"title": "Test Title", "description": "This is a test post", "published": True, "content": "some content"}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_upload_image(self):
        # TODO Use a more stable file than the twitter logos in mapApp
        self.client.login(username="test_superuser", password="password")

        # Test jpeg
        img = open( "mapApp/static/mapApp/images/BikeMapsTwitterLogo.jpg", "rb")
        response = self.client.post("/blog/upload_image/", {"title":"Test image", "image": img , "resize": 1000})
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        img.close()

        # Test png
        img = open( "mapApp/static/mapApp/images/BikeMapsTwitterLogo.png", "rb")
        response = self.client.post("/blog/upload_image/", {"title":"Test image", "image": img , "resize": 1000})
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        img.close()

def create_user():
    return User.objects.create_user("test_user", email="user@bikemaps.org", password="password")

def create_superuser():
    return User.objects.create_superuser("test_superuser", email="super_user@bikemaps.org", password="password")
