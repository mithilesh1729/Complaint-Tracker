from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Complaint, ComplaintImage, StatusLog


# ✅ Custom User Admin
class UserAdmin(BaseUserAdmin):
    # Fields jo add/edit form mein dikhenge
    fieldsets = (
        (None, {'fields': ('roll_no', 'password')}),
        ('Personal Info', {'fields': ('hostel', 'room_no', 'email')}),
        ('Permissions', {'fields': ('is_admin', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('roll_no', 'password1', 'password2', 'hostel', 'room_no', 'email', 'is_admin'),
        }),
    )
    list_display = ('roll_no', 'hostel', 'room_no', 'email', 'is_admin')  # Columns jo list view mein dikhenge
    search_fields = ('roll_no', 'email')  # Search bar ke liye fields
    list_filter = ('is_admin', 'hostel')  # Filters sidebar mein
    ordering = ('roll_no',)  # Default sorting

# ✅ Complaint Admin
class ComplaintImageInline(admin.TabularInline):  # Inline images in Complaint admin
    model = ComplaintImage
    extra = 1  # Kitne blank image fields dikhenge by default
    readonly_fields = ('uploaded_at',)  # uploaded_at editable nahi hoga

class StatusLogInline(admin.TabularInline):  # Inline status logs in Complaint admin
    model = StatusLog
    extra = 0  # No extra blank fields—sirf existing logs dikhenge
    readonly_fields = ('status', 'message', 'timestamp')  # Sab read-only
    can_delete = False  # Logs delete nahi hone chahiye

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    # List view display fields
    list_display = ('complaint_id', 'user', 'complaint_type', 'colored_status', 'priority', 'created_at')
    list_filter = ('status', 'priority', 'complaint_type', 'created_at')  # Filters
    search_fields = ('complaint_id', 'description', 'user__roll_no')  # Search by ID, description, roll_no
    inlines = [ComplaintImageInline, StatusLogInline]  # Images aur logs inline dikhenge
    list_per_page = 20  # Pagination—20 complaints per page
    ordering = ('-created_at',)  # Latest complaints pehle

    # Detail view ke liye fields customize karte hai
    fieldsets = (
        (None, {'fields': ('complaint_id', 'user', 'complaint_type', 'description')}),
        ('Status & Priority', {'fields': ('status', 'priority', 'resolved_at')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    readonly_fields = ('complaint_id', 'created_at', 'updated_at', 'resolved_at')  # Yeh editable nahi honge

    # Date-based navigation
    date_hierarchy = 'created_at'  # Admin panel mein date-based navigation enable karega

    # Custom filtering based on user permissions (Only showing complaints for non-superusers)
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:  # Non-superuser ke liye sirf unke complaints dikhayenge
            qs = qs.filter(user=request.user)
        return qs

    # Status ko color code karna
    def colored_status(self, obj):
        color_map = {
            'Pending': 'red',
            'In Progress': 'orange',
            'Resolved': 'green',
        }
        return format_html('<span style="color: {};">{}</span>', color_map.get(obj.status, 'black'), obj.status)

    colored_status.allow_tags = True
    colored_status.admin_order_field = 'status'  # Sorting ke liye enable

# ✅ ComplaintImage Admin
@admin.register(ComplaintImage)
class ComplaintImageAdmin(admin.ModelAdmin):
    list_display = ('complaint', 'image', 'uploaded_at')
    search_fields = ('complaint__complaint_id',)
    list_filter = ('uploaded_at',)
    readonly_fields = ('uploaded_at',)

# ✅ StatusLog Admin
@admin.register(StatusLog)
class StatusLogAdmin(admin.ModelAdmin):
    list_display = ('complaint', 'status', 'message', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('complaint__complaint_id', 'message')
    readonly_fields = ('timestamp',)
    ordering = ('-timestamp',)

# Register User model with custom admin
admin.site.register(User, UserAdmin)
