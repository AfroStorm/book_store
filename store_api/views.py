from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from store_api import serializers
from rest_framework.decorators import action
from store_api import models
from django.contrib.auth.models import User
from store_api.permissions import IsListOnly, IoRoProfile, IoRoUser,\
    IoRoOrder
from rest_framework.permissions import IsAuthenticatedOrReadOnly
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

    @action(detail=True, methods=['PATCH'])
    def update_wishlist(self, request, pk=None):
        '''
        Adds or removes a product from the profile wishlist. Requires a
        key value pair of "action": "remove" or "add" and "product_id": "pk"
        in the request body
        '''

        product_id = self.request.data.get('product_id')
        product = get_object_or_404(models.Product, pk=product_id)
        profile = self.get_object()

        action = self.request.data.get('action')
        if action == 'add':
            profile.wishlist.add(product)
        elif action == 'remove':
            profile.wishlist.remove(product)
        else:
            return Response(
                {'detail': '"action" is neither "add" nor "remove" (kwarg)'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer(
            profile,
            data={'wishlist': profile.wishlist},
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class OrderVIew(ModelViewSet):
    '''
    Displays the Order in a browsable api
    '''

    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IoRoOrder, IsAuthenticatedOrReadOnly,]

    def perform_create(self, serializer):
        '''
        Checks if request is POST to associate the profile field of the 
        Order with the profile of the authenticated user
        '''
        if self.request.method == 'POST':
            serializer.validated_data['profile'] = self.request.user.profile

        return super().perform_create(serializer)


class LoginView(ObtainAuthToken):
    '''
    Handles creating user authentication tokens
    '''

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
