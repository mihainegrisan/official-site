from django.db.models.signals import post_save # the signal
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

# Create a profile for every new user when they register for an account

# When a user is saved, then send post_save signal that's gonna be received by the receiver(the create_profile function).
# post_save signal passes (instance and created) arguments to the receiver.
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# instance is the user that wants to register
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
