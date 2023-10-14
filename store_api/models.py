from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.caption


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
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

    lenght = models.FloatField(null=True)
    height = models.FloatField(null=True)
    width = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    rating = models.IntegerField(null=True)
    color = models.CharField(max_length=50, null=True)
    publishing_date = models.DateField(null=True)
    author = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'Category: {self.category}\n Product name{self.name}'


class Profile(models.Model):
    address = models.CharField(max_length=255)
    customer = models.OneToOneField(
        User,
        on_delete=models.CASCADE
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
        return f'{self.customer.username}'
