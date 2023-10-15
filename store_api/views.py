from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from store_api import serializers
from store_api import models
# Create your views here.


class TagView(ModelViewSet):
    '''
    Displays the tags in a browsable api
    '''

    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
