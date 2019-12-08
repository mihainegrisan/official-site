from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from django.template.defaultfilters import slugify
from django.db import IntegrityError
from .utils import unique_slugify
import re
from django.utils.safestring import mark_safe


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICE = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    tags = TaggableManager()

    objects = models.Manager() # The default manager
    published = PublishedManager() # My custom manager

    title = models.CharField(max_length=80)
    # slug = models.SlugField(max_length=200, unique_for_date='date_published')
    slug = models.SlugField(max_length=200, unique=True)
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

    def save(self, *args, **kwargs):
        unique_slugify(self, self.title)
        super(Post, self).save(**kwargs)

    def get_absolute_url(self):
        return reverse('blog:post-detail',
                       args=[self.date_published.year,
                             self.date_published.month,
                             self.date_published.day,
                             self.slug])

    def get_time_to_read(self):
        # result = list(map(lambda x: x.strip(), self.content.split(' ')))
        result = len(re.findall(r'\w+', self.content))
        return result // 150 + 1

    # returns the full url to the instance as a string
    # def get_absolute_url(self):
    #     return reverse('blog:post-detail',
    #                    kwargs={
    #                         'year': self.date_published.year,
    #                         'month': self.date_published.month,
    #                         'day': self.date_published.day,
    #                         'slug': self.slug
    #                         })
