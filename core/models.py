from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone
import uuid
from django.db.models import Count


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
    PENDING = "pending", "Pending"
    IN_PROGRESS = "in_progress", "In Progress"
    RESOLVED = "resolved", "Resolved"
    ESCALATED_WARDEN = "escalated_warden", "Escalated to Warden"
    ESCALATED_HMC = "escalated_hmc", "Escalated to HMC"



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

    def create_superuser(
        self,
        roll_no,
        email=None,
        password=None,
        **extra_fields,
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)

        # Temporary until Platform Admin is introduced.
        extra_fields.setdefault(
            "role",
            UserRole.HOSTEL_OFFICE,
        )

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
    
    
     
class ComplaintQuerySet(models.QuerySet):
    """
    Reusable query helpers for Complaint.
    """

    def pending(self):
        return self.filter(
            status=ComplaintStatus.PENDING,
        )

    def in_progress(self):
        return self.filter(
            status=ComplaintStatus.IN_PROGRESS,
        )

    def resolved(self):
        return self.filter(
            status=ComplaintStatus.RESOLVED,
        )

    def confirmed(self):
        return self.filter(
            is_confirmed=True,
        )

    def unresolved(self):
        return self.exclude(
            status=ComplaintStatus.RESOLVED,
        )

    def escalated_warden(self):
        return self.filter(
            status=ComplaintStatus.ESCALATED_WARDEN,
        )
        
    def escalated_hmc(self):
        return self.filter(
            status=ComplaintStatus.ESCALATED_HMC,
        )

    def high_priority(self):
        return self.filter(
            priority=ComplaintPriority.HIGH,
        )

    def unassigned(self):
        return self.filter(
            assigned_to__isnull=True,
        )

    def assigned(self):
        return self.exclude(
            assigned_to__isnull=True,
        )

    def for_user(self, user):
        return self.filter(
            user=user,
        )

    def assigned_to(self, user):
        return self.filter(
            assigned_to=user,
        )

    def latest(self):
        return self.order_by(
            "-created_at",
        )

    def with_related(self):
        return self.select_related(
            "user",
            "category",
            "assigned_to",
        )

    def dashboard_stats(self):
        """
        Aggregate statistics for Student Dashboard.
        """

        stats = self.aggregate(
            total=Count("id"),

            pending=Count(
                "id",
                filter=models.Q(
                    status=ComplaintStatus.PENDING,
                ),
            ),

            in_progress=Count(
                "id",
                filter=models.Q(
                    status=ComplaintStatus.IN_PROGRESS,
                ),
            ),

            resolved=Count(
                "id",
                filter=models.Q(
                    status=ComplaintStatus.RESOLVED,
                ),
            ),
        )

        stats["active"] = (
            stats["pending"] +
            stats["in_progress"]
        )

        return stats
    
    

# =====================================================
# Complaint Model
# =====================================================
class Complaint(models.Model):
    
    objects = ComplaintQuerySet.as_manager()
    # ---------- Legacy Choices (Will be removed in V3) ----------
    STATUS_CHOICES = ComplaintStatus.choices

    PRIORITY_CHOICES = ComplaintPriority.choices

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
        choices=ComplaintStatus.choices,
        default=ComplaintStatus.PENDING,
    )

    priority = models.CharField(
        max_length=20,
        choices=ComplaintPriority.choices,
        default=ComplaintPriority.MEDIUM,
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
    # Escalation Remarks
    # =====================================================
    
    warden_remark = models.TextField(blank=True)
    hmc_remark = models.TextField(blank=True)

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
            models.Index(fields=["user", "status"]),
            models.Index(fields=["assigned_to"]),
            models.Index(fields=["complaint_number"]),
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
    status = models.CharField(
        max_length=20,
        choices=ComplaintStatus.choices,
    )
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