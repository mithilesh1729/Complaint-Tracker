from rest_framework import permissions

from core.models import UserRole

from rest_framework.permissions import BasePermission


class RolePermission(BasePermission):
    allowed_roles = ()

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in self.allowed_roles
        )

class IsHostelOffice(RolePermission):
    allowed_roles = (UserRole.HOSTEL_OFFICE,)


class IsStudent(RolePermission):
    allowed_roles = (UserRole.STUDENT,)


class IsWarden(RolePermission):
    allowed_roles = (UserRole.WARDEN,)


class IsHMC(RolePermission):
    allowed_roles = (UserRole.HMC,)


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_superuser
        )


class CanViewComplaint(permissions.BasePermission):
    """
    Controls who can view a complaint.

    Allowed:
    - Complaint owner (Student)
    - Assigned Hostel Office
    - Admin

    Later:
    - Warden
    - HMC
    """

    def has_object_permission(
        self,
        request,
        view,
        obj,
    ):
        user = request.user

        # Admin
        if user.is_admin:
            return True

        # Student who created complaint
        if obj.user == user:
            return True

        # Hostel Office can view complaints from their hostel
        if user.role == UserRole.HOSTEL_OFFICE and obj.hostel == user.hostel:
            return True
            
        # Warden can view complaints from their hostel
        if user.role == UserRole.WARDEN and obj.hostel == user.hostel:
            return True
            
        # HMC can view all complaints
        if user.role == UserRole.HMC:
            return True

        return False