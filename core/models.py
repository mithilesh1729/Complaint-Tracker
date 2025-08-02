from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
# from django.utils import timezone
import datetime
import uuid

# ✅ Custom User Manager (for superuser creation)
class CustomUserManager(UserManager):
    def create_superuser(self, roll_no, email, password=None, **extra_fields):
        """
        Create and return a superuser with roll_no, email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not roll_no:
            raise ValueError('The roll_no field must be set')
        if not email:
            raise ValueError('The Email field must be set')

        user = self.model(roll_no=roll_no, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

# ✅ Custom User Model (For Students & Admin)
class User(AbstractUser):
    roll_no = models.CharField(max_length=20, unique=True, primary_key=True)
    name = models.CharField(max_length=100, default="Unknown")
    hostel = models.CharField(max_length=50, default="Unknown")  
    room_no = models.CharField(max_length=10, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField('auth.Group', related_name='core_user_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='core_user_permissions', blank=True)

    USERNAME_FIELD = 'roll_no'  
    REQUIRED_FIELDS = ['email'] 

    # Custom User Manager
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        if not self.username:  # Assign roll_no as username if empty
            self.username = self.roll_no  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.roll_no} - {self.name}"

# ✅ Complaint Model (For Tracking Complaints)
class Complaint(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    )

    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    TYPE_CHOICES = (
        ('mess', 'Mess'),
        ('electricity', 'Electricity'),
        ('water', 'Water'),
        ('other', 'Other'),
    )

    complaint_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')  
    name = models.CharField(max_length=100)  # Manually entered
    hostel = models.CharField(max_length=50)  # Manually entered
    room_no = models.CharField(max_length=10)  # Manually entered
    phone_number = models.CharField(max_length=15)  # Manual entry

    complaint_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.status == 'resolved' and not self.resolved_at:
            # self.resolved_at = timezone.now()
            self.resolved_at = datetime.datetime.now()  # Use naive datetime
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.complaint_id} - {self.complaint_type} ({self.status})"

    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]


# ✅ Complaint Image Model
class ComplaintImage(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='complaints/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.complaint.complaint_id}"  

# ✅ Status Log Model
class StatusLog(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='status_logs')
    status = models.CharField(max_length=20, choices=Complaint.STATUS_CHOICES)
    message = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.complaint.complaint_id} - {self.status} at {self.timestamp}"

# ✅ Django Signal for Auto-Log Complaint Status Changes
from django.db.models.signals import post_save
from django.dispatch import receiver 

@receiver(post_save, sender=Complaint)
def create_status_log(sender, instance, created, **kwargs):
    if created:
        StatusLog.objects.create(
            complaint=instance,
            status=instance.status,
            message="Complaint created with initial status"
        )
