# StaffAPIView

# StaffResetPasswordAPIView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from core.services.user_service import UserService

from core.models import User
from core.serializers import StaffSerializer




class StaffAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if not request.user.is_admin:
            return Response(
                {"detail": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN,
            )

        staff = User.objects.filter(
            role__in=[
                "hostel_office",
                "warden",
                "hmc",
            ],
            is_superuser=False,
            is_admin=False
        ).order_by("roll_no")

        serializer = StaffSerializer(
            staff,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):

        if not request.user.is_admin:
            return Response(
                {"detail": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = StaffSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        staff = serializer.save()

        return Response(
            {
                "message": "Staff created successfully. Credentials sent via email.",
                "roll_no": staff.roll_no,
            },
            status=status.HTTP_201_CREATED,
        )    

    def patch(self, request, roll_no):
        if not request.user.is_admin:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
            
        staff = get_object_or_404(User, roll_no=roll_no)
        
        serializer = StaffSerializer(staff, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
            
        return Response({"message": "Staff updated successfully."})
        
    def delete(self, request, roll_no):
        if not request.user.is_admin:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)
            
        staff = get_object_or_404(User, roll_no=roll_no)
        if staff.is_active:
            UserService.deactivate(staff)
        else:
            UserService.activate(staff)
        
        action = "activated" if staff.is_active else "deactivated"
        return Response({"message": f"Staff {action} successfully."})


class StaffResetPasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, roll_no):

        if not request.user.is_admin:
            return Response(
                {"detail": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN,
            )

        user = get_object_or_404(
            User,
            roll_no=roll_no,
        )

        # Safety check
        if user.role not in [
            "hostel_office",
            "warden",
            "hmc",
        ]:
            return Response(
                {"detail": "Not a staff account."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        from core.services.staff_service import StaffService
        user, temp_password = StaffService.reset_password(user)

        return Response(
            {
                "message": "Password reset successfully. Credentials sent via email."
            }
        )