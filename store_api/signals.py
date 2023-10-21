from django.contrib.auth.models import User
from store_api.models import Profile, Order
from django.dispatch import receiver
from django.db.models.signals import post_save
from celery import shared_task
from time import sleep


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    '''
    Creates a profile and saves the user in itś Customer field
    '''
    if created:
        Profile.objects.create(customer=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    '''
    Saves the newly created UserProfile
    '''
    instance.profile.save()


@shared_task
def check_payment_confirmations():
    '''
    Checks the pending payments
    '''

    unprocessed_payments = Order.objects.filter(is_confirmed=False)

    for order in unprocessed_payments:
        sleep(5)
        # Simulate checking for order confirmation (you would use the
        # actual order gateway API)
        # If order is confirmed, set is_confirmed=True
        order.is_confirmed = True
        order.save()
