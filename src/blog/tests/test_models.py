from django.test import TestCase
from blog.models import Post, PublishedManager
from django.contrib.auth.models import User
from django.utils import timezone


class TestModels(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(
            username = 'mihai'
        )

        self.post1 = Post.objects.create(
            title = 'Title old',
            tags = ['jazz'],
            # slug = 'title-old',
            author = self.user1,
            content = 'I just bought some stocks. ad as as k kkkkkssaaaa aads adsadasfsfas sfaassdadsadadsaa waaaaaaaaaaaaaaaaaa aaaaaaaaaaaaaaa aaaaaaaaaaaa aaaaaaaaaaaaaaaa aaaaaaaaaaa fafa sf as asf',
            date_published = timezone.now(),
            date_created = '2015-09-04 06:00',
            date_updated = '2015-09-04 06:00',
            status = 'published',
        )
        self.post2 = Post.objects.create(
            title = 'Title new',
            tags = ['rap'],
            # slug = 'title-new',
            author = self.user1,
            content = 'I just bought some artwork.',
            date_published = '2012-09-04 06:00:00.000000-08:00',
            date_created = '2012-09-04 06:00',
            date_updated = '2012-09-04 06:00',
            status = 'draft',
        )

    def test_fields(self):
        post3 = Post.objects.create(
            title = 'Some title',
            tags = ['pop'],
            # slug = 'title-new',
            author = self.user1,
            content = 'I just bought some tea.',
            date_published = '2012-09-04 06:00:00.000000-08:00',
            date_created = '2012-09-04 06:00',
            date_updated = '2012-09-04 06:00',
            status = 'draft',
        )
        record = Post.objects.get(id=post3.id)
        self.assertEquals(record, post3)

    # testing the save() method
    def test_post_is_assigned_unique_slug_on_creation(self):
        self.assertEquals(self.post1.slug, 'title-old')

    def test_get_absolute_url(self):
        t = timezone.now()
        url = f'/blog/post/{t.year}/{t.month}/{t.day}/title-old/'
        self.assertEquals(self.post1.get_absolute_url(), url)

    def test_get_time_to_read(self):
        self.assertEquals(self.post1.get_time_to_read(), 2)

    def test_published_manager_filters_correctly(self):
        qs = Post.objects.filter(status='published')
        qs_published = Post.published.all()
        self.assertQuerysetEqual(qs_published, [repr(r) for r in qs])
