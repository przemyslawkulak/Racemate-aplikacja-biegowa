from rest_framework import permissions

from racemate.models import RunningGroup


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.

        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the admin of the group.
        print(obj.admins == request.user.id)
        return obj.admins == request.user.id
