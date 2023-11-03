from rest_framework import permissions
from store_api import views


class IsOwner(permissions.BasePermission):
    '''
    Checks if the request user is the authenticated owner. obj.customer
    (user).
    '''

    def has_object_permission(self, request, view, obj):
        '''
        Checks for the obj.customer (user).
        '''

        return (
            request.user and request.user.is_authenticated and
            request.user == obj.customer
        )


class IsUser(permissions.BasePermission):
    '''
    Checks if the request user is the authenticated owner of the user
    intsance.
    '''

    def has_object_permission(self, request, view, obj):

        return (
            request.user and request.user.is_authenticated and
            request.user == obj
        )


class IsReadOnly(permissions.BasePermission):
    '''
    Only allows readonly methods.
    '''

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS
