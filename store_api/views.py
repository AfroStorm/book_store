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


class UpdateWishlistView(generics.UpdateAPIView):
    '''
    Adds or removes a product from the profile wishlist. Requires a
    key value pair of "action": "remove" or "add" and "product_id": "pk"
    in the request body
    '''
    queryset = models.Profile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IoRoProfile]
    serializer_class = serializers.ProfileSerializer

    def perform_update(self, serializer):
        '''
        Checks if the product should be added or removed
        from wishlist
        '''
        product_id = self.request.data.get('product_id')
        profile = self.get_object()
        product = self.does_exist(product_id)
        action = self.request.data.get('action')

        if action == 'remove':
            profile.wishlist.remove(product)

        elif action == 'add':
            profile.wishlist.add(product)

        else:
            return Response(
                {'detail': '"action" is neither "add" nor "remove" (kwarg)'},
                status=status.HTTP_400_BAD_REQUEST
            )

        wishlist = profile.wishlist.all()
        serializer.save(wishlist=wishlist)

    def does_exist(self, product_id):
        '''
        Checks if the product is in database or sends http404 product not
        found
        '''
        try:
            product = models.Product.objects.get(pk=product_id)
            return product
        except models.Product.DoesNotExist:
            raise Http404('Product not found')


class LoginView(ObtainAuthToken):
    '''
    Handles creating user authentication tokens
    '''

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
