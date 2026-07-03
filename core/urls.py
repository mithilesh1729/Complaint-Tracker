from django.urls import path
from .views import *

urlpatterns = [
    path('complaints/', ComplaintListView.as_view(), name='complaint-list'),
    path('complaints/create/', complaint_create, name='complaint-create'),
    path('complaints/<uuid:complaint_id>/', complaint_detail, name='complaint-detail'),
    path('complaints/<uuid:complaint_id>/update/', complaint_update, name='complaint-update'),
    path('complaints/<uuid:complaint_id>/delete/', complaint_delete, name='complaint-delete'),
    path("complaints/<uuid:complaint_id>/logs/",complaint_logs,name="complaint-logs"),
    path("complaints/<uuid:complaint_id>/slip/",download_complaint_slip,name="complaint-slip"),
    path("complaints/<uuid:complaint_id>/confirm/",confirm_complaint_resolution,name="complaint-confirm"),

]


urlpatterns += [
    path(
        "students/",
        StudentAPIView.as_view(),
        name="student-list-create",
    ),
    path(
        "students/<str:roll_no>/",
        StudentAPIView.as_view(),
        name="student-detail",
    ),
    path(
        "students/<str:roll_no>/reset-password/",
        StudentResetPasswordAPIView.as_view(),
        name="student-reset-password",
    ),
]