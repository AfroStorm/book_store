from django.contrib.auth.models import User
from store_api import models
from django.dispatch import receiver
from django.db.models.signals import post_save


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    '''
    Creates a profile and saves the user in itś Customer field
    '''

    if created:
        models.Profile.objects.create(customer=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    '''
    Saves the newly created UserProfile in the userprofile field of the newly
    created User
    '''
    instance.profile.save()
