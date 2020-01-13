from django.test import TestCase, Client
from django.urls import reverse
from blog.models import Post
from django.contrib.auth.models import User
from django.utils import timezone
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.post_list_url = reverse('blog:post_list')
        self.post_list_by_tag = reverse('blog:post_list_by_tag', args=['jazz'])

        self.user1 = User.objects.create(
            username = 'mihai',
        )

        Post.objects.create(
            title = 'Socks party',
            tags = ['jazz'],
            author = self.user1,
            content = 'I just bought some socks.',
            date_published = timezone.now(),
            date_created = '2015-09-04 06:00',
            date_updated = '2015-09-04 06:00',
            status = 'published',
        )

    def test_post_list_GET(self):
        # Test code
        response = self.client.get(self.post_list_url)

        # Assertions
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_post_list_by_tag_GET(self):
        # Test code
        print(self.post_list_by_tag)
        response = self.client.get(self.post_list_by_tag)

        # Assertions
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_post_detail_GET(self):
        pass
