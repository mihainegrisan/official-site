from django.test import SimpleTestCase
# use anytime you don't need to interact with the database
from django.urls import reverse, resolve
from blog import views
from blog.views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
)

class TestUrls(SimpleTestCase):

    def test_post_list_url_is_resolved(self):
        url = reverse('blog:post_list')
        # print(resolve(url))
        self.assertEquals(resolve(url).func, views.post_list)

    def test_post_list_by_tag_url_is_resolved(self):
        url = reverse('blog:post_list_by_tag', args=['pretty-slug'])
        self.assertEquals(resolve(url).func, views.post_list)

    def test_user_posts_url_is_resolved(self):
        url = reverse('blog:user-posts', args=['mihai'])
        self.assertEquals(resolve(url).func.view_class, UserPostListView)

    def test_post_detail_url_is_resolved(self):
        url = reverse('blog:post-detail', args=['2019', '11', '29', 'pretty-slug'])
        self.assertEquals(resolve(url).func.view_class, PostDetailView)

    def test_post_create_url_is_resolved(self):
        url = reverse('blog:post-create')
        self.assertEquals(resolve(url).func.view_class, PostCreateView)

    def test_post_update_url_is_resolved(self):
        url = reverse('blog:post-update', args=['12'])
        self.assertEquals(resolve(url).func.view_class, PostUpdateView)

    def test_post_delete_url_is_resolved(self):
        url = reverse('blog:post-delete', args=['12'])
        self.assertEquals(resolve(url).func.view_class, PostDeleteView)

    def test_post_share_by_email_url_is_resolved(self):
        url = reverse('blog:post_share_by_email', args=['12'])
        self.assertEquals(resolve(url).func, views.post_share)

    def test_about_url_is_resolved(self):
        url = reverse('blog:about')
        self.assertEquals(resolve(url).func, views.about)
