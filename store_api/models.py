from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

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


class ProductReviewHistory(models.Model):
    '''
    Review history for each product
    '''

    overall_rating = models.DecimalField(
        decimal_places=1,
        max_digits=2,
        default=0.0,
        validators=[
            MaxValueValidator(5.0),
            MinValueValidator(0.0),
        ]
    )
    sumarized_ratings = models.FloatField(default=0.0)
    number_of_voters = models.IntegerField(default=0)

    def calculate_rating(self, customer_rating=None):
        '''
        Adds a customer rating and calculates the overall rating for a
        product, limiting it to a maximum of 5.0 and returns it. If no 
        customer_rating is given it also returns the overall rating of
        the product.
        '''

        if customer_rating is not None:
            self.number_of_voters += 1
            self.sumarized_ratings += customer_rating

        if self.number_of_voters > 0:
            overall_rating = (self.sumarized_ratings /
                              self.number_of_voters) * 5.0
            return min(round(overall_rating, 1), 5.0)
        else:
            # Return 0.0 if there are no voters (to avoid division by zero)
            return 0.0

    def __str__(self) -> str:
        return f' {self.product.name} review history'


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
    review_history = models.OneToOneField(
        ProductReviewHistory,
        related_name='product',
        on_delete=models.CASCADE,
        null=True
    )

    lenght = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
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
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(max_length=255, blank=True)

    customer = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    wishlist = models.ManyToManyField(
        Product,
        related_name='wishlist',
    )

    def __str__(self) -> str:
        '''
        Displays the object as a string
        '''
        return f'{self.customer.username}'


class CustomerReview(models.Model):
    '''
    Single Review of a product
    '''

    rating = models.FloatField()
    review_text = models.TextField(blank=True, max_length=1000)
    date = models.DateField(auto_now_add=True)

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='product_reviews',
        null=True
    )
    product = models.ForeignKey(
        Product,
        related_name='reviews',
        on_delete=models.CASCADE,
        null=True
    )
    review_history = models.ForeignKey(
        ProductReviewHistory,
        related_name='product_reviews',
        on_delete=models.CASCADE,
        null=True
    )

    def __str__(self) -> str:
        return f'{self.customer.username} product-review'


class Order(models.Model):
    '''
    Pending order of a customer. Waits for payment confirmation.
    '''

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    products = models.ManyToManyField(
        Product,
        related_name='products'
    )
    date_of_ordering = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)
