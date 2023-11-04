from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from store_api.models import Profile, Order, Product, ProductReviewHistory
from django.dispatch import receiver
from django.db.models.signals import post_save
from celery import shared_task
from time import sleep


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    '''
    Creates a profile instance for each newly created product instance.
    '''
    if created:
        Profile.objects.create(
            customer=instance,
            first_name=instance.first_name,
            last_name=instance.last_name,
            email=instance.email,
            last_login=instance.last_login,
            date_joined=instance.date_joined
        )


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    '''
    Saves the newly created UserProfile
    '''
    instance.profile.save()


@receiver(post_save, sender=Product)
def create_review_history(sender, instance, created, **kwargs):
    '''
    Creates a review history instance for each newly created product
    instance.
    '''

    if created:
        ProductReviewHistory.objects.create(product=instance)


@receiver(post_save, sender=Product)
def save_review_history(sender, instance, **kwargs):
    '''
    Saves the created review history instance and puts it in relation with
    the product instance.
    '''

    instance.review_history.save()


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
