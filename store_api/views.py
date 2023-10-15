from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from store_api import serializers
from store_api import models
from django.contrib.auth.models import User
from store_api.permissions import IsListOnly, IoRoProfile, IoRoUser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticatedOrReadOnly
# Create your views here.


class TagView(ModelViewSet):
    '''
    Displays the tags in a browsable api
    '''

    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = [IsListOnly,]


class CategoryView(ModelViewSet):
    '''
    Displays the category in a browsable api
    '''

    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsListOnly,]


class ProductView(ModelViewSet):
    '''
    Displays the product in a browsable api
    '''

    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsListOnly,]


class UserView(ModelViewSet):
    '''
    Displays the user in a browsable api
    '''

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IoRoUser,]


class ProfileView(ModelViewSet):
    '''
    Displays the profile in a browsable api
    '''

    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsListOnly, IoRoProfile]


class LoginView(ObtainAuthToken):
    '''
    Handles creating user authentication tokens
    '''

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
