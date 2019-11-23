from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from django.urls import reverse
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICE = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    tags = TaggableManager()

    # def get_absolute_url(self):
    #     return reverse('blog:post_detail',
    #                    args=[self.publish.year,
    #                          self.publish.month,
    #                          self.publish.day,
    #                          self.slug])

    objects = models.Manager() # The default manager
    published = PublishedManager() # My custom manager

    title = models.CharField(max_length=125)
    slug = models.SlugField(max_length=200, unique_for_date='date_published')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    # if I'll use auto_now_add=True I won't be able to change the date so
    # pass the timezone.now function as default value but don't execute it
    date_published = models.DateTimeField(default=timezone.now)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='draft')

    class Meta:
        ordering = ('-date_published', )

    def __str__(self):
        return self.title
