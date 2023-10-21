from rest_framework import serializers
from store_api import models
from django.contrib.auth.models import User


class TagSerializer(serializers.ModelSerializer):
    '''
    Serializes the tag model.
    '''

    class Meta:
        model = models.Tag
        fields = ['caption']
        extra_kwargs = {
            'caption': {'read_only': True}
        }


class CategorySerializer(serializers.ModelSerializer):
    '''
    Serializes the category models.
    '''
    class Meta:
        model = models.Category
        fields = ['name']
        extra_kwargs = {
            'name': {'read_only': True}
        }


class ProductSerializer(serializers.ModelSerializer):
    '''
    Serializes the product model
    '''
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='caption'
    )
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = models.Product
        fields = '__all__'
        read_only_fields = ('__all__',)


class UserSerializer(serializers.ModelSerializer):
    '''
    Serializes the user 
    '''
    profile = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'email', 'first_name', 'last_name',
            'profile'

        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }


class ProfileSerializer(serializers.ModelSerializer):
    '''
    Serializes the profile
    '''

    class Meta:
        model = models.Profile
        fields = [
            'id', 'address', 'last_login', 'date_joined', 'customer',
            'purchase_history', 'wishlist'
        ]
        extra_kwargs = {
            'purchase_history': {'read_only': True},
            'wishlist': {'read_only': True},
            'customer': {'read_only': True},
        }


class PendingOrderSerializer(serializers.ModelSerializer):
    '''
    Serializes the PendingOrder model
    '''
    products = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.Product.objects.all()
    )

    class Meta:
        model = models.PendingOrder
        fields = [
            'id', 'products', 'profile', 'date_of_ordering', 'is_confirmed'
        ]
        read_only_fields = ('profile', 'is_confirmed',)
