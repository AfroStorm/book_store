from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from store_api import serializers
from store_api import models
from django.contrib.auth.models import User
from store_api.permissions import IsListOnly, IoRoProfile, IoRoUser
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

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
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IoRoUser,]


class ProfileView(ModelViewSet):
    '''
    Displays the profile in a browsable api
    '''

    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsListOnly, IoRoProfile]


class AddToWishlistView(generics.UpdateAPIView):
    '''
    Adds a product to the profile wishlist
    '''
    queryset = models.Profile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IoRoProfile]
    serializer_class = serializers.ProfileSerializer

    def perform_update(self, serializer):
        '''
        Gets product id from the request body and checks if the product exists.
        Then gets the user profile from authenticated user and adds the product to the wishlist.
        '''

        product_id = self.request.data.get('product_id')
        try:
            product = models.Product.objects.get(pk=product_id)
        except models.Product.DoesNotExist:
            return Response({'detail': 'Product not found!'},
                            status=status.HTTP_404_NOT_FOUND)

        profile = self.get_object()
        profile.wishlist.add(product)
        wishlist = profile.wishlist.all()
        serializer.save(wishlist=wishlist)


class LoginView(ObtainAuthToken):
    '''
    Handles creating user authentication tokens
    '''

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
