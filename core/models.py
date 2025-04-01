from django.db import models
from django.contrib.auth.models import AbstractUser

from django.utils import timezone
import uuid
# Create your models here.
# ✅ Custom User Model (For Students & Admin)
class User(AbstractUser):
    roll_no = models.CharField(max_length=20, unique=True, primary_key=True)  # 🎯 Roll number as primary key (Unique Student ID)
    hostel = models.CharField(max_length=50, blank=True)  # 🎯 Hostel Name
    room_no = models.CharField(max_length=10, blank=True)  # 🎯 Room Number
    email = models.EmailField(unique=True, blank=True, null=True)  # 🎯 Unique email for notifications
    is_admin = models.BooleanField(default=False)  # 🎯 Role-based access (Student/Admin)

    # Yeh do lines add karo
    groups = models.ManyToManyField('auth.Group', related_name='core_user_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='core_user_permissions', blank=True)
    

    USERNAME_FIELD = 'roll_no'  # 🎯 Login using Roll Number
    REQUIRED_FIELDS = ['username']  # 🎯 Required field for Django Admin

    def __str__(self):
        return self.roll_no


# ✅ Complaint Model (For Tracking Complaints)
class Complaint(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),  # 🎯 Complaint is yet to be addressed
        ('in_progress', 'In Progress'),  # 🎯 Complaint is being resolved
        ('resolved', 'Resolved'),  # 🎯 Complaint is successfully resolved
    )

    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),  # 🎯 Priority levels for sorting complaints
    )

    TYPE_CHOICES = (
        ('mess', 'Mess'),
        ('electricity', 'Electricity'),
        ('water', 'Water'),
        ('other', 'Other'),  # 🎯 Different complaint categories
    )
    
    complaint_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # 🎯 Unique ID for tracking
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')  # 🎯 Link to the student
    complaint_type = models.CharField(max_length=20, choices=TYPE_CHOICES)  # 🎯 Type of complaint
    description = models.TextField()  # 🎯 Detailed complaint description
    
    # photo = models.ImageField(upload_to='complaints/%Y/%m/%d/', null=True, blank=True)  # 🎯 Optional image upload
 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # 🎯 Status of complaint
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')  # 🎯 Priority of issue
    created_at = models.DateTimeField(auto_now_add=True)  # 🎯 Automatic timestamp when complaint is created
    updated_at = models.DateTimeField(auto_now=True)  # 🎯 Timestamp when complaint is modified
    resolved_at = models.DateTimeField(null=True, blank=True)  # 🎯 Stores the resolution time

    # ✅ Automatically update resolved_at when complaint is marked as resolved
    def save(self, *args, **kwargs):
        if self.status == 'resolved' and not self.resolved_at:
            self.resolved_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.complaint_id} - {self.complaint_type} ({self.status})"

    class Meta:
        indexes = [
            models.Index(fields=['status']),  # 🎯 Faster queries on status filtering
            models.Index(fields=['created_at']),  # 🎯 Optimize sorting by complaint date
        ]
        

# ✅ Complaint Image Model (For Supporting Multiple Photos)
class ComplaintImage(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name="images")  # 🎯 Link to complaint
    image = models.ImageField(upload_to='complaints/%Y/%m/%d/')  # 🎯 Store images in a structured format
    uploaded_at = models.DateTimeField(auto_now_add=True)  # 🎯 Timestamp for when the image was uploaded

    def __str__(self):
        return f"Image for {self.complaint.complaint_id}"  

           
# ✅ Status Log Model (For Tracking Complaint Progress)
class StatusLog(models.Model):
    complaint = models.ForeignKey(Complaint, on_delete=models.CASCADE, related_name='status_logs')  # 🎯 Link to complaint
    status = models.CharField(max_length=20, choices=Complaint.STATUS_CHOICES)  # 🎯 Stores status updates
    message = models.TextField(blank=True)  # 🎯 Admin response (e.g., "Will resolve in 2 days")
    timestamp = models.DateTimeField(auto_now_add=True)  # 🎯 When status was updated

    def __str__(self):
        return f"{self.complaint.complaint_id} - {self.status} at {self.timestamp}"



# ✅ Django Signal (Auto-Log Complaint Status Changes)
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
                      