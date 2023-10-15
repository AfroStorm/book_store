from rest_framework import permissions


class ReadOnly(permissions.BasePermission):
    '''
    Sets the list view to read only
    '''

    def has_permission(self, request, view):
        '''
        Checks for the methods in the request
        '''
        return request.method == permissions.SAFE_METHODS
