from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Allow access if user is admin or object owner.
    Assumes obj has a `.user` field.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_admin:
            return True
        return obj.user == request.user