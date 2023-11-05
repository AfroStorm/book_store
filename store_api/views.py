from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from store_api import serializers
from rest_framework.decorators import action
from store_api import models
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from store_api.permissions import IsOwner, IsReadOnly, IsUser
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter

# Create your views here.


class TagView(ModelViewSet):
    '''
    Displays the tags in a browsable api
    '''

    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAdminUser | IsReadOnly]
    filter_backends = [SearchFilter,]
    search_fields = ['caption',]


class CategoryView(ModelViewSet):
    '''
    Displays the category in a browsable api
    '''

    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAdminUser | IsReadOnly]
    filter_backends = [SearchFilter,]
    search_fields = ['name',]


class ProductView(ModelViewSet):
    '''
    Displays the product in a browsable api
    '''

    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAdminUser | IsReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'name', 'description', 'tags', 'author']
    ordering_fields = [
        'id', 'category', 'price', 'tags', 'publishing_date', 'author'
    ]


class ProductReviewHistory(ModelViewSet):
    '''
    Displays the product review history in a browsable api
    '''

    queryset = models.ProductReviewHistory.objects.all()
    serializer_class = serializers.ProductReviewHistorySerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAdminUser | IsReadOnly]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'overall_rating', 'product']
    ordering_fields = ['id', 'overall_rating', 'product']


class CustomerReviewView(ModelViewSet):
    '''
    Displays the product in a browsable api
    '''

    queryset = models.CustomerReview.objects.all()
    serializer_class = serializers.CustomerReviewSerializer
    authentication_classes = (TokenAuthentication,)
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        'id', 'rating', 'date', 'customer', 'product'
    ]
    ordering_fields = ['id', 'rating', 'customer',]

    def get_permissions(self):
        '''
        Implements permission classes for different view actions.
        '''
        if self.action == 'create':
            permission_classes = [IsAdminUser | IsAuthenticated]

        elif self.action == 'update' or\
                self.action == 'partial_update' or\
                self.action == 'destroy':
            permission_classes = [IsAdminUser | IsOwner]

        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        '''
        Assign the request user to the customer field. Admin users
        are excluded from this.
        '''

        if not self.request.user.is_staff:
            serializer.validated_data['customer'] = self.request.user

        return super().perform_create(serializer)


class UserView(ModelViewSet):
    '''
    Displays the user in a browsable api
    '''

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    authentication_classes = (TokenAuthentication,)
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'email', 'date_joined', 'last_login']
    ordering_fields = ['id', 'username', 'date_joined', 'last_login']

    def get_permissions(self):
        '''
        Implements permission classes for different view actions.
        '''
        if self.action == 'update' or\
                self.action == 'partial_update' or\
                self.action == 'destroy':
            permission_classes = [IsAdminUser | IsUser]

        else:
            permission_classes = []

        return [permission() for permission in permission_classes]


class ProfileView(ModelViewSet):
    ''' 
    Displays the profile in a browsable api.
    '''

    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    authentication_classes = (TokenAuthentication,)
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['id', 'first_name', 'last_name', 'email', 'customer']
    ordering_fields = [
        'id', 'last_login', 'date_joined', 'first_name', 'last_name',
        'customer'
    ]

    def get_permissions(self):
        '''
        Implements permission classes for different view actions.
        '''
        if self.action == 'create':
            permission_classes = [IsAdminUser,]

        elif self.action == 'update' or\
                self.action == 'partial_update' or\
                self.action == 'destroy':
            permission_classes = [IsAdminUser | IsOwner]

        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['PATCH'])
    def update_wishlist(self, request, pk=None):
        '''
        Adds or removes a product from the profile wishlist. Requires a
        key value pair of "command": "remove" or "add" and "product_id": "pk"
        in the request body.
        '''

        product_id = self.kwargs['pk']
        product = get_object_or_404(models.Product, pk=product_id)
        profile = self.get_object()
        command = self.request.data.get('command')

        if command == 'add':
            profile.wishlist.add(product)
        elif command == 'remove':
            profile.wishlist.remove(product)
        else:
            return Response(
                {'detail': '"command" is neither "add" nor "remove" (kwarg)'},
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


class OrderView(ModelViewSet):
    '''
    Displays the Order in a browsable api
    '''

    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    authentication_classes = (TokenAuthentication,)
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = [
        'id', 'customer', 'products', 'date_of_ordering', 'is_confirmed'
    ]
    ordering_fields = [
        'id', 'customer', 'products', 'date_of_ordering', 'is_confirmed'
    ]

    def get_queryset(self):
        '''
        Excludes non owners from viewing other users orders, except admin.
        '''

        if self.request.user.is_staff:
            return super().get_queryset()

        owner_id = self.request.user.id
        queryset = models.Order.objects.filter(pk=owner_id)
        return queryset

    def get_permissions(self):
        '''
        Implements permission classes for different view actions.
        '''
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAdminUser | IsAuthenticated]

        elif self.action == 'create':
            permission_classes = [IsAdminUser | IsAuthenticated]

        elif self.action == 'update' or\
                self.action == 'partial_update' or\
                self.action == 'destroy':
            permission_classes = [IsAdminUser | IsOwner]

        else:
            permission_classes = []

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        '''
        Assign the request user to the customer field. Admin users
        are excluded from this.
        '''

        if not self.request.user.is_staff:
            serializer.validated_data['customer'] = self.request.user

        return super().perform_create(serializer)


class LoginView(ObtainAuthToken):
    '''
    Handles creating user authentication tokens
    '''

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
