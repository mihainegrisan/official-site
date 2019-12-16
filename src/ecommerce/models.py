from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import reverse
from blog.utils import unique_slugify
from django.utils.text import slugify

CATEGORY_CHOICES = (
('S', 'Shirt'),
('SW', 'Sport wear'),
('OW', 'Outwear'),
)

LABEL_CHOICES = (
('P', 'primary'),
('S', 'secondary'),
('D', 'danger'),
)

class Item(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    description = models.TextField()


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ecommerce:product', kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse('ecommerce:add-to-cart', kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse('ecommerce:remove-from-cart', kwargs={
            'slug': self.slug
        })

    # def save(self, *args, **kwargs):
    #     # unique_slugify(self, self.title)
    #     # super(Item, self).save(**kwargs)
    #     value = self.title
    #     self.slug = slugify(value, allow_unicode=True)
    #     super().save(*args, **kwargs)


class CartItem(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             blank=True,
                             null=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.quantity} of {self.item.title}'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
