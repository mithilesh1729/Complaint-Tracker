from django.urls import path
from .views import *

urlpatterns = [
    # path('complaints/', ComplaintListAPIView.as_view(), name='complaint-list'),
    # path('complaints/create/', complaint_create, name='complaint-create'),
    # path('complaints/<uuid:complaint_id>/', complaint_detail, name='complaint-detail'),
    # path('complaints/<uuid:complaint_id>/update/', complaint_update, name='complaint-update'),
    # path('complaints/<uuid:complaint_id>/delete/', complaint_delete, name='complaint-delete'),
    # path("complaints/<uuid:complaint_id>/logs/",complaint_logs,name="complaint-logs"),
    # path("complaints/<uuid:complaint_id>/slip/",download_complaint_slip,name="complaint-slip"),
    # path("complaints/<uuid:complaint_id>/confirm/",confirm_complaint_resolution,name="complaint-confirm"),

]


urlpatterns += [
    path(
        "complaints/",
        ComplaintListAPIView.as_view(),
    ),
    path(
        "complaints/create/",
        ComplaintCreateAPIView.as_view(),
    ),

    path(
        "complaints/<uuid:complaint_id>/",
        ComplaintDetailAPIView.as_view(),
    ),

    path(
        "complaints/<uuid:complaint_id>/delete/",
        ComplaintDeleteAPIView.as_view(),
    ),

    path(
        "complaint-categories/",
        ComplaintCategoryListAPIView.as_view(),
    ),
    path(
        "complaints/<uuid:complaint_id>/logs/",
        ComplaintLogsAPIView.as_view(),
    ),
    path(
        "complaints/<uuid:complaint_id>/slip/",
        ComplaintSlipAPIView.as_view(),
    ),
    
    
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
    path(
        "office/queue/",
        HostelQueueAPIView.as_view(),
        name="office-queue",
    ),
    path(
        "complaints/<uuid:complaint_id>/assign/",
        AssignComplaintAPIView.as_view(),
        name="assign-complaint",
    ),
    path(
        "office/my-complaints/",
        MyAssignedComplaintsAPIView.as_view(),
        name="my-assigned-complaints",
    ),
    path(
        "staff/",
        StaffAPIView.as_view(),
        name="staff-management",
    ),
    path(
        "staff/<str:roll_no>/reset-password/",
        StaffResetPasswordAPIView.as_view(),
        name="staff-reset-password",
    ),
    path(
        "complaint-categories/",
        ComplaintCategoryListAPIView.as_view(),
        name="complaint-categories",
    ),
    path(
        "complaints/<uuid:complaint_id>/resolve/",
        ResolveComplaintAPIView.as_view(),
        name="resolve-complaint",
    ),
    path(
        "complaints/<uuid:complaint_id>/progress/",
        UpdateComplaintProgressAPIView.as_view(),
        name="update-complaint-progress",
    ),
    path(
        "complaints/<uuid:complaint_id>/reopen/",
        ReopenComplaintAPIView.as_view(),
        name="reopen-complaint",
    ),
    path(
        "profile/",
        ProfileAPIView.as_view(),
        name="profile",
    ),
    
    path(
        "student/dashboard/",
        StudentDashboardAPIView.as_view(),
        name="student-dashboard",
    ),
]