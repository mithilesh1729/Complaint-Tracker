from django.contrib import admin

from .models import (
    User,
    Department,
    Hostel,
    ComplaintCategory,
    HostelAssignment,
    Complaint,
    ComplaintImage,
    StatusLog,
)


# =====================================================
# Department
# =====================================================
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "is_active",
    )

    search_fields = (
        "code",
        "name",
    )

    list_filter = (
        "is_active",
    )


# =====================================================
# Hostel
# =====================================================
@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "office_phone",
        "is_active",
    )

    search_fields = (
        "name",
    )

    list_filter = (
        "is_active",
    )


# =====================================================
# Complaint Category
# =====================================================
@admin.register(ComplaintCategory)
class ComplaintCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "display_order",
        "name",
        "is_active",
    )

    ordering = (
        "display_order",
    )

    search_fields = (
        "name",
    )

    list_filter = (
        "is_active",
    )


# =====================================================
# Hostel Assignment
# =====================================================
@admin.register(HostelAssignment)
class HostelAssignmentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "hostel",
        "room_no",
        "from_date",
        "to_date",
        "is_current",
    )

    list_filter = (
        "hostel",
        "is_current",
    )

    search_fields = (
        "user__roll_no",
        "user__name",
    )


# =====================================================
# User
# =====================================================
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "roll_no",
        "name",
        "role",
        "department",
        "hostel",
        "room_no",
        "is_active",
    )

    search_fields = (
        "roll_no",
        "name",
        "email",
    )

    list_filter = (
        "role",
        "department",
        "is_active",
    )


# =====================================================
# Complaint
# =====================================================
@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = (
        "complaint_number",
        "complaint_type",
        "status",
        "priority",
        "user",
        "assigned_to",
        "created_at",
    )

    search_fields = (
        "complaint_number",
        "user__roll_no",
        "user__name",
    )

    list_filter = (
        "status",
        "priority",
        "complaint_type",
    )


# =====================================================
# Complaint Image
# =====================================================
@admin.register(ComplaintImage)
class ComplaintImageAdmin(admin.ModelAdmin):
    list_display = (
        "complaint",
        "uploaded_at",
    )


# =====================================================
# Status Log
# =====================================================
@admin.register(StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    list_display = (
        "complaint",
        "status",
        "timestamp",
    )