# StudentAPIView

# StudentResetPasswordAPIView


from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser
from core.selectors.student_selector import StudentSelector
from core.services.student_service import StudentService

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView



from core.models import Hostel
from core.serializers import StudentListSerializer,StudentCreateSerializer,StudentUpdateSerializer





class StudentAPIView(GenericAPIView):

    permission_classes = [IsAdminUser]

    def get(self, request, roll_no=None):

        if roll_no:
            student = StudentSelector.get_student_or_404(roll_no)

            serializer = StudentListSerializer(student)

            return Response(serializer.data)

        is_active_param = request.query_params.get("is_active")
        is_active = None
        if is_active_param:
            if is_active_param.lower() == "true":
                is_active = True
            elif is_active_param.lower() == "false":
                is_active = False

        queryset = StudentSelector.list_students(
            search=request.query_params.get("search"),
            department=request.query_params.get("department"),
            hostel=request.query_params.get("hostel"),
            is_active=is_active,
        )

        page = self.paginate_queryset(queryset)

        serializer = StudentListSerializer(
            page,
            many=True,
        )

        return self.get_paginated_response(serializer.data)

    def post(self, request):

        serializer = StudentCreateSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        student = serializer.save()

        return Response(
            {
                "message": "Student created successfully. Credentials sent via email.",
                "roll_no": student.roll_no,
            },
            status=status.HTTP_201_CREATED,
        )       
        
    
    def patch(self, request, roll_no):

        student = StudentSelector.get_student_or_404(roll_no)

        serializer = StudentUpdateSerializer(
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        StudentService.update_student(
            user=student,
            name=data.get("name", student.name),
            email=data.get("email", student.email),
            phone_number=data.get(
                "phone_number",
                student.phone_number,
            ),
            department=data.get(
                "department",
                student.department,
            ),
        )

        if (
            "hostel" in data
            or "room_no" in data
        ):
            StudentService.transfer_hostel(
                user=student,
                hostel=data.get("hostel", Hostel.objects.get(name=student.hostel)),
                room_no=data.get("room_no", student.room_no),
            )

        return Response(
            {
                "message": "Student updated successfully."
            }
        )  
  
    def delete(self, request, roll_no):
        student = StudentSelector.get_student_or_404(roll_no)

        if student.is_active:
            from core.services.user_service import UserService
            UserService.deactivate(student)
        else:
            from core.services.user_service import UserService
            UserService.activate(student)
            
        action = "activated" if student.is_active else "deactivated"

        return Response(
            {
                "message": f"Student {action} successfully."
            }
        )
        






class StudentResetPasswordAPIView(APIView):

    permission_classes = [IsAdminUser]
    
    def post(self, request, roll_no):
        student = StudentSelector.get_student_or_404(roll_no)

        user, password = StudentService.reset_password(student)
        
        return Response(
            {
                "message": "Password reset successfully. Credentials sent via email."
            }
        ) 