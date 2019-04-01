from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        print(obj.owner, request.user)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the admin of the group.
        return obj.owner == request.user
