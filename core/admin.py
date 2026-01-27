from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Complaint, ComplaintImage, StatusLog


# =====================================================
# User Admin
# =====================================================
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("roll_no", "password")}),
        ("Personal Info", {"fields": ("name", "hostel", "room_no", "email")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_admin",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "roll_no",
                    "password1",
                    "password2",
                    "name",
                    "hostel",
                    "room_no",
                    "email",
                    "is_admin",
                ),
            },
        ),
    )

    list_display = (
        "roll_no",
        "name",
        "hostel",
        "room_no",
        "email",
        "is_admin",
        "is_staff",
        "is_active",
    )
    search_fields = ("roll_no", "name", "email")
    list_filter = ("is_admin", "is_staff", "is_active", "hostel")
    ordering = ("roll_no",)


# =====================================================
# Inline: Complaint Images
# =====================================================
class ComplaintImageInline(admin.TabularInline):
    model = ComplaintImage
    extra = 0
    readonly_fields = ("uploaded_at",)


# =====================================================
# Inline: Status Logs
# =====================================================
class StatusLogInline(admin.TabularInline):
    model = StatusLog
    extra = 0
    readonly_fields = ("status", "message", "timestamp")
    can_delete = False


# =====================================================
# Complaint Admin
# =====================================================
@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = (
        "complaint_id",
        "user",
        "complaint_type",
        "colored_status",
        "priority",
        "created_at",
    )

    list_filter = (
        "status",
        "priority",
        "complaint_type",
        "created_at",
    )

    search_fields = ("complaint_id", "description", "user__roll_no")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    readonly_fields = (
        "complaint_id",
        "created_at",
        "updated_at",
        "resolved_at",
    )

    fieldsets = (
        (
            "Complaint Details",
            {
                "fields": (
                    "complaint_id",
                    "user",
                    "name",
                    "hostel",
                    "room_no",
                    "complaint_type",
                    "description",
                )
            },
        ),
        (
            "Status & Priority",
            {"fields": ("status", "priority", "resolved_at")},
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    inlines = [ComplaintImageInline, StatusLogInline]

    # -------------------------
    # UI helper (Django 6 safe)
    # -------------------------
    def colored_status(self, obj):
        if not obj or not obj.status:
            return "-"

        color_map = {
            "pending": "#dc3545",      # red
            "in_progress": "#fd7e14",  # orange
            "resolved": "#198754",     # green
        }

        return format_html(
            '<span style="font-weight:600; color:{};">{}</span>',
            color_map.get(obj.status, "#000"),
            obj.get_status_display(),
        )

    colored_status.short_description = "Status"
    colored_status.admin_order_field = "status"


# =====================================================
# Complaint Image Admin
# =====================================================
@admin.register(ComplaintImage)
class ComplaintImageAdmin(admin.ModelAdmin):
    list_display = ("complaint", "image", "uploaded_at")
    search_fields = ("complaint__complaint_id",)
    list_filter = ("uploaded_at",)
    readonly_fields = ("uploaded_at",)


# =====================================================
# Status Log Admin
# =====================================================
@admin.register(StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    list_display = ("complaint", "status", "message", "timestamp")
    list_filter = ("status", "timestamp")
    search_fields = ("complaint__complaint_id", "message")
    readonly_fields = ("timestamp",)
    ordering = ("-timestamp",)


# =====================================================
# Register User
# =====================================================
admin.site.register(User, UserAdmin)
