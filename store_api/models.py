from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tag(models.Model):
    '''
    Highlights the product with different tags.
    '''
    caption = models.CharField(max_length=20)

    def __str__(self) -> str:
        '''
        Displays the object as a string.
        '''
        return self.caption


class Category(models.Model):
    '''
    Indicates the category in which the product fits in.
    '''
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        '''
        Displays the object as a string.
        '''
        return self.name


class Product(models.Model):
    '''
    The product in the online shop has different properties depending on its
    category. Some properties are required, others are optional.
    '''
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    image = models.CharField(
        max_length=500,
        default='https://i0.wp.com/blankhans.io/wp-content/uploads/2021/08/'
        'placeholder.png?fit=1200%2C800&ssl=1'
    )
    price = models.FloatField()
    description = models.TextField()
    tags = models.ManyToManyField(Tag)

    lenght = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    publishing_date = models.DateField(null=True, blank=True)
    author = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self) -> str:
        '''
        Displays the object as a string.
        '''
        return f'Category: {self.category}\n/ Name: {self.name}'


class Profile(models.Model):
    '''
    Profile that shows additional information about the customer.
    Also contains a personal purchase history and a wishlist of prducts.
    '''
    address = models.CharField(max_length=255)
    last_login = models.DateField(null=True)
    date_joined = models.DateField(null=True)
    customer = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    purchase_history = models.ManyToManyField(
        Product,
        related_name='purchase_history'
    )
    wishlist = models.ManyToManyField(
        Product,
        related_name='wishlist'
    )

    def __str__(self) -> str:
        '''
        Displays the object as a string
        '''
        return f'{self.customer.username}'


class PendingOrder(models.Model):
    '''
    Pending order of a customer. Waits for payment confirmation.
    '''
    profile = models.ForeignKey(
        Profile,
        related_name='pending_orders'
    )
    products = models.ManyToManyField(
        Product,
        related_name='products'
    )
    date_of_ordering = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
