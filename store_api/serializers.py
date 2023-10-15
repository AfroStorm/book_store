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
