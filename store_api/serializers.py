from rest_framework import serializers
from store_api import models


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
