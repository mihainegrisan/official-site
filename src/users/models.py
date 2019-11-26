from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


    # image resize when user adds it to their profile
    # Not gonna work with S3 buckets !
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs) # call the save method of the parent
    #
    #     img = Image.open(self.image.path) # the image of the current instance
    #
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300, 300)
    #         img.thumbnail(output_size)
    #         img.save(self.image.path) # override the previous image
