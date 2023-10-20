from django.contrib.auth.models import User
from store_api.models import Profile, PendingOrder
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


@receiver(post_save, sender=PendingOrder)
def is_payed(instance, **kwargs):
    '''
    Checks if the payment is confirmed. Adds products to purchase history.
    Removes products from pending orders.
    '''
    if instance.is_confirmed:
        products_list = instance.products.all()
        profile = instance.profile

        profile.purchase_history.add(*products_list)
        profile.pending_orders.remove(*products_list)


@shared_task
def check_payment_confirmations():
    '''
    Checks the pending payments
    '''

    unprocessed_payments = PendingOrder.objects.filter(is_confirmed=False)

    for payment in unprocessed_payments:
        sleep(5)
        # Simulate checking for payment confirmation (you would use the
        # actual payment gateway API)
        # If payment is confirmed, set is_confirmed=True
        payment.is_confirmed = True
        payment.save()
