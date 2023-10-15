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


class CategoryView(ModelViewSet):
    '''
    Displays the category in a browsable api
    '''

    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer


class ProductView(ModelViewSet):
    '''
    Displays the product in a browsable api
    '''

    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
