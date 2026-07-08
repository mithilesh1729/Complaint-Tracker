from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone
import uuid



# =====================================================
# Abstract Base Model
# =====================================================
class TimeStampedModel(models.Model):
    """
    Reusable timestamp fields for all master/business models.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# =====================================================
# User Roles
# =====================================================
class UserRole(models.TextChoices):
    STUDENT = "student", "Student"
    HOSTEL_OFFICE = "hostel_office", "Hostel Office"
    WARDEN = "warden", "Hostel Warden"
    HMC = "hmc", "Hostel Management Committee"
    # SUPER_ADMIN = "super_admin", "Super Admin"


# =====================================================
# Complaint Priority
# =====================================================
class ComplaintPriority(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"


# =====================================================
# Complaint Status
# =====================================================
class ComplaintStatus(models.TextChoices):
    SUBMITTED = "submitted", "Submitted"
    UNDER_REVIEW = "under_review", "Under Review"
    IN_PROGRESS = "in_progress", "In Progress"
    RESOLVED = "resolved", "Resolved"
    WAITING_CONFIRMATION = "waiting_confirmation", "Waiting Student Confirmation"
    CLOSED = "closed", "Closed"
    REOPENED = "reopened", "Reopened"



# =====================================================
# Department (Master Data)
# =====================================================
class Department(TimeStampedModel):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"


# =====================================================
# Hostel (Master Data)
# =====================================================
class Hostel(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    office_phone = models.CharField(max_length=15, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# =====================================================
# Complaint Category (Master Data)
# =====================================================
class ComplaintCategory(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name_plural = "Complaint Categories"

    def __str__(self):
        return self.name



# # Custom User Manager
# # =====================================================
# class CustomUserManager(UserManager):
#     def create_superuser(self, roll_no, email, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)

#         if not roll_no:
#             raise ValueError("The roll_no field must be set")
#         if not email:
#             raise ValueError("The Email field must be set")

#         user = self.model(roll_no=roll_no, email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user



class CustomUserManager(UserManager):
    def create_user(self, roll_no, email=None, password=None, **extra_fields):
        if not roll_no:
            raise ValueError("The roll_no field must be set")

        user = self.model(
            roll_no=roll_no,
            username=roll_no,
            email=self.normalize_email(email) if email else None,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, roll_no, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        # Temporary
        extra_fields.setdefault("is_admin", True)

        # New Role System
        extra_fields.setdefault("role", UserRole.SUPER_ADMIN)

        return self.create_user(
            roll_no,
            email,
            password,
            **extra_fields,
        )


# Custom User Model
# =====================================================
class User(AbstractUser):
    roll_no = models.CharField(max_length=20, primary_key=True)

    name = models.CharField(
        max_length=100,
        default="Unknown",
    )

    # Legacy fields (will be removed after HostelAssignment migration)
    hostel = models.CharField(
        max_length=50,
        default="Unknown",
    )

    room_no = models.CharField(
        max_length=10,
        blank=True,
    )

    email = models.EmailField(
        unique=True,
        null=True,
        blank=True,
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True,
    )

    # Keep temporarily for backward compatibility
    is_admin = models.BooleanField(default=False)

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.STUDENT,
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="users",
    )

    must_change_password = models.BooleanField(
        default=True,
    )

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="core_user_groups",
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="core_user_permissions",
        blank=True,
    )

    USERNAME_FIELD = "roll_no"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.roll_no

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.roll_no} - {self.name}"
    
    
    
    
    
    
    
    # =====================================================
# Hostel Assignment
# =====================================================
class HostelAssignment(TimeStampedModel):
    """
    Maintains hostel history of every user.
    Students:
        - hostel
        - room number
    Hostel Office / Warden:
        - hostel only
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="hostel_assignments",
    )

    hostel = models.ForeignKey(
        Hostel,
        on_delete=models.PROTECT,
        related_name="assignments",
    )

    room_no = models.CharField(
        max_length=10,
        blank=True,
    )

    from_date = models.DateField()

    to_date = models.DateField(
        null=True,
        blank=True,
    )

    is_current = models.BooleanField(default=True)

    class Meta:
        ordering = ["-from_date"]

    def __str__(self):
        return f"{self.user.roll_no} → {self.hostel.name}"
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

# =====================================================
# Complaint Model
# =====================================================
class Complaint(models.Model):

    # ---------- Legacy Choices (Will be removed in V3) ----------
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
    )

    PRIORITY_CHOICES = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    )

    TYPE_CHOICES = (
        ("mess", "Mess"),
        ("electricity", "Electricity"),
        ("water", "Water"),
        ("other", "Other"),
    )

    # =====================================================
    # Identity
    # =====================================================

    complaint_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    # Student visible complaint number
    complaint_number = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True,
        editable=False,
    )

    # =====================================================
    # Relationships
    # =====================================================

    # Student who created complaint
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="complaints",
    )

    # Future replacement of complaint_type
    category = models.ForeignKey(
        ComplaintCategory,
        on_delete=models.PROTECT,
        related_name="complaints",
        null=True,
        blank=True,
    )

    # Hostel Office Staff handling complaint
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="assigned_complaints",
        null=True,
        blank=True,
    )

    # =====================================================
    # Snapshot Fields
    # (Keep history even if student profile changes)
    # =====================================================

    name = models.CharField(max_length=100)

    hostel = models.CharField(max_length=50)

    room_no = models.CharField(max_length=10)

    phone_number = models.CharField(max_length=15)

    # Extra location
    location_details = models.CharField(
        max_length=200,
        blank=True,
    )

    # =====================================================
    # Complaint Details
    # =====================================================

    # Legacy (Will migrate to category)
    complaint_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
    )

    description = models.TextField()

    # =====================================================
    # Workflow
    # =====================================================

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium",
    )

    # =====================================================
    # Timeline
    # =====================================================

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    closed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    # =====================================================
    # Student Confirmation
    # =====================================================

    is_confirmed = models.BooleanField(default=False)

    confirmed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    student_feedback = models.TextField(blank=True)

    # =====================================================
    # Internal Status Tracking
    # =====================================================

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_status = self.status

    def save(self, *args, **kwargs):

        if self.status == "resolved" and not self.resolved_at:
            self.resolved_at = timezone.now()

        super().save(*args, **kwargs)

        self._original_status = self.status

    def __str__(self):
        return f"{self.complaint_number or self.complaint_id} - {self.status}"

    class Meta:
        indexes = [
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["priority"]),
        ]


# Complaint Images
# =====================================================
class ComplaintImage(models.Model):
    complaint = models.ForeignKey(
        Complaint, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="complaints/%Y/%m/%d/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.complaint.complaint_id}"



# Status Log 
# =====================================================
class StatusLog(models.Model):
    complaint = models.ForeignKey(
        Complaint, on_delete=models.CASCADE, related_name="status_logs"
    )
    status = models.CharField(max_length=20, choices=Complaint.STATUS_CHOICES)
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.complaint.complaint_id} - {self.status} at {self.timestamp}"







# Super Admin (Platform)
#         │
#         ├───────────────┐
#         │               │
#         ▼               ▼
# Students          Staff Users
#                        │
#       ┌────────────────┼──────────────┐
#       ▼                ▼              ▼
# Hostel Office       Warden           HMC