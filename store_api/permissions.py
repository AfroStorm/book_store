from rest_framework import permissions


class IsListOnly(permissions.BasePermission):
    """
    Only allows read on a list (has_permission)
    """

    def has_permission(self, request, view):
        """
        Checks if view.action is create
        """

        return view.action != 'create'


class IoRoUser(permissions.BasePermission):
    '''
    IsOwnerOrReadOnly on user (has_object_permission)
    '''

    def has_object_permission(self, request, view, obj):
        '''
        Checks if the request user is the same as the user object
        '''
        if request.method == permissions.SAFE_METHODS:
            return True

        return request.user.id == obj.id


class IoRoProfile(permissions.BasePermission):
    '''
    IsOwnerOrReadOnly on profile (has_object_permission)
    '''

    def has_object_permission(self, request, view, obj):
        '''
        Checks if the request user is the owner of the profile
        '''
        if request.method == permissions.SAFE_METHODS:
            return True

        elif view.action == 'CREATE':
            return True

        return request.user == obj.customer


class IoRoProfile(permissions.BasePermission):
    '''
    IsOwnerOrReadOnly on profile (has_object_permission)
    '''

    def has_object_permission(self, request, view, obj):
        '''
        Checks if the request user is the owner of the profile
        '''
        if request.method == permissions.SAFE_METHODS:
            return True

        return request.user == obj.customer


class IoRoOrder(permissions.BasePermission):
    '''
    IsOwnerOrReadOnly on PendingOrder (has_object_permission)
    '''

    def has_object_permission(self, request, view, obj):
        '''
        Checks if the request user is the owner of the profile
        '''
        if request.method == permissions.SAFE_METHODS:
            return True

        return request.user.profile == obj.profile
