from rest_framework import serializers, permissions
from store_api import models
from django.contrib.auth.models import User


class TagSerializer(serializers.ModelSerializer):
    '''
    Serializes the tag model.
    '''

    class Meta:
        model = models.Tag
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    '''
    Serializes the category models.
    '''
    class Meta:
        model = models.Category
        fields = '__all__'


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


class UserSerializer(serializers.ModelSerializer):
    '''
    Serializes the user 
    '''
    profile = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'username', 'password', 'first_name', 'last_name', 'email',
            'last_login', 'date_joined', 'profile'
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            },
        }

    def get_fields(self):
        '''
        Prevents the request user from manually filling out fields that are
        supposed to be handled by other sources. Except admin.
        '''
        request = self.context['request']
        fields = super().get_fields()

        if request.method not in permissions.SAFE_METHODS:
            if not request.user.is_staff:
                read_only_fields = ['last_login', 'date_joined', 'profile']
                for field in read_only_fields:
                    fields[field].read_only = True

                return fields

        return fields

    def to_representation(self, instance):
        '''
        Checks if the request user is the owner. Prevents sensitive
        information from being displayed to non authorized requests.
        '''

        request = self.context['request']
        data = super().to_representation(instance)

        if request.user.is_staff or request.user.is_superuser:
            return data

        if request.user != instance:

            fields_to_omit = [
                'first_name', 'last_name', 'email', 'last_login'
            ]
            for field in fields_to_omit:
                data.pop(field, None)

        return data


class ProfileSerializer(serializers.ModelSerializer):
    '''
    Serializes the profile
    '''

    class Meta:
        model = models.Profile
        fields = '__all__'

    def update(self, instance, validated_data):
        '''
        Checks if the request user is staff. Prevents the owner from
        modifying sensitive business relevant data.
        '''

        request_user = self.context['request'].user
        if request_user.is_staff or request_user.is_superuser:
            return super().update(instance, validated_data)

        allowed_fields = [
            'address', 'first_name', 'last_name', 'email', 'wishlist'
        ]
        for field in allowed_fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])

        instance.save()
        return instance

    def to_representation(self, instance):
        '''
        Checks if the request user is the owner. Prevents sensitive
        information from being displayed to non authorized requests.
        '''

        request_user = self.context['request'].user
        data = super().to_representation(instance)

        if request_user.is_staff or request_user.is_superuser:
            return data

        if request_user != instance.customer:

            fields_to_omit = [
                'orders', 'wishlist', 'last_login', 'email', 'address',
                'first_name', 'last_name'
            ]
            for field in fields_to_omit:
                data.pop(field, None)

        return data


class OrderSerializer(serializers.ModelSerializer):
    '''
    Serializes the Order model
    '''

    products = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.Product.objects.all()
    )

    class Meta:
        model = models.Order
        fields = '__all__'


class ProductReviewHistorySerializer(serializers.ModelSerializer):
    '''
    Serializes the product history
    '''

    class Meta:
        model = models.ProductReviewHistory
        fields = '__all__'
        read_only_fields = ('__all__',)


class CustomerReviewSerializer(serializers.ModelSerializer):
    '''
    Serializes the customer review
    '''

    class Meta:
        model = models.CustomerReview
        fields = '__all__'
        read_only_fields = ('__all__',)
