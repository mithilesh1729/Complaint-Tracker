from django.urls import path
from .views import *
from core.views.department_views import DepartmentManagementAPIView


urlpatterns = [
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
        OfficeQueueAPIView.as_view(),
        name="office-queue",
    ),
    path(
        "office/complaints/<uuid:complaint_id>/assign/",
        AssignComplaintAPIView.as_view(),
        name="assign-complaint",
    ),
    path(
        "office/assigned/",
        OfficeAssignedComplaintsAPIView.as_view(),
        name="office-assigned",
    ),
    path(
        "staff/",
        StaffAPIView.as_view(),
        name="staff-management",
    ),
    path(
        "staff/<str:roll_no>/",
        StaffAPIView.as_view(),
        name="staff-detail",
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
        "admin/categories/",
        CategoryManagementAPIView.as_view(),
        name="admin-categories",
    ),
    path(
        "admin/categories/<int:category_id>/",
        CategoryManagementAPIView.as_view(),
        name="admin-category-detail",
    ),
    path(
        "admin/reports/csv/",
        AdminReportAPIView.as_view(),
        name="admin-reports-csv",
    ),
    path(
        "admin/hostels/",
        HostelManagementAPIView.as_view(),
        name="admin-hostels-list",
    ),
    path(
        "admin/hostels/<int:hostel_id>/",
        HostelManagementAPIView.as_view(),
        name="admin-hostel-detail",
    ),
    path(
        "admin/departments/",
        DepartmentManagementAPIView.as_view(),
        name="admin-departments-list",
    ),
    path(
        "admin/departments/<int:department_id>/",
        DepartmentManagementAPIView.as_view(),
        name="admin-department-detail",
    ),
    path(
        "office/complaints/<uuid:complaint_id>/resolve/",
        ResolveComplaintAPIView.as_view(),
        name="resolve-complaint",
    ),
    path(
        "complaints/<uuid:complaint_id>/progress/",
        UpdateComplaintProgressAPIView.as_view(),
        name="update-complaint-progress",
    ),
    path(
        "office/complaints/<uuid:complaint_id>/escalate/",
        EscalateToWardenAPIView.as_view(),
        name="escalate-complaint",
    ),
    path(
        "complaints/<uuid:complaint_id>/reopen/",
        ReopenComplaintAPIView.as_view(),
        name="reopen-complaint",
    ),
    path(
        "complaints/<uuid:complaint_id>/confirm/",
        ConfirmComplaintResolutionAPIView.as_view(),
        name="confirm-complaint",
    ),
    path(
        "profile/",
        ProfileAPIView.as_view(),
        name="profile",
    ),
    path(
        "profile/password/",
        ChangePasswordAPIView.as_view(),
        name="change-password",
    ),
    
    path(
        "student/dashboard/",
        StudentDashboardAPIView.as_view(),
        name="student-dashboard",
    ),
    
    path(
        "office/dashboard/",
        OfficeDashboardAPIView.as_view(),
        name="office-dashboard",
    ),
    
    path(
        "admin/dashboard/",
        AdminDashboardAPIView.as_view(),
        name="admin-dashboard",
    ),
    
    # ==========================
    # Warden API
    # ==========================
    path("warden/dashboard/", WardenDashboardAPIView.as_view(), name="warden-dashboard"),
    path("warden/queue/", WardenQueueAPIView.as_view(), name="warden-queue"),
    path("warden/staff-performance/", WardenStaffPerformanceAPIView.as_view(), name="warden-staff-performance"),
    path("warden/complaints/<uuid:complaint_id>/action/", WardenComplaintActionAPIView.as_view(), name="warden-action"),

    # ==========================
    # HMC API
    # ==========================
    path("hmc/dashboard/", HMCDashboardAPIView.as_view(), name="hmc-dashboard"),
    path("hmc/queue/", HMCQueueAPIView.as_view(), name="hmc-queue"),
    path("hmc/hostel-performance/", HMCHostelPerformanceAPIView.as_view(), name="hmc-hostel-performance"),
    path("hmc/complaints/<uuid:complaint_id>/action/", HMCComplaintActionAPIView.as_view(), name="hmc-action"),
]