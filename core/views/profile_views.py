# ProfileAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from core.serializers import ProfileSerializer

class ProfileAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)    

    def patch(self, request):
        # Allow updating name, phone_number
        user = request.user
        data = request.data
        
        user.name = data.get("name", user.name)
        user.phone_number = data.get("phone_number", user.phone_number)
        
        user.save(update_fields=["name", "phone_number"])
        
        serializer = ProfileSerializer(user)
        return Response(serializer.data)


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            return Response(
                {"detail": "Both old and new passwords are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not user.check_password(old_password):
            return Response(
                {"detail": "Incorrect old password."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if old_password == new_password:
            return Response(
                {"detail": "New password cannot be the same as the old password."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        import re
        if len(new_password) < 8 or not re.search(r"[A-Za-z]", new_password) or not re.search(r"\d", new_password):
            return Response(
                {"detail": "Password must be at least 8 characters long and contain both letters and numbers."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        # Assuming admin might have must_change_password set, let's clear it
        user.must_change_password = False
        user.save(update_fields=["password", "must_change_password"])

        return Response({"message": "Password changed successfully."})