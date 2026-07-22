from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_credentials_email_task(user_email, name, raw_password, is_reset=False):
    """
    Sends an email to the user with their login credentials.
    Runs asynchronously via Celery.
    """
    
    subject = "Hostel Complaint Tracker - Password Reset" if is_reset else "Welcome to Hostel Complaint Tracker"
    
    action = "reset" if is_reset else "created"
    
    message = f"""
Hello {name},

Your account for the NIT Patna Hostel Complaint Tracking System has been {action}.

Please log in using your Roll Number/ID and the temporary password below:

Temporary Password: {raw_password}

For security reasons, you MUST change your password immediately after logging in by navigating to your Profile page.

Regards,
Hostel Management Centre
National Institute of Technology Patna
    """
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )

@shared_task
def send_complaint_status_email_task(user_email, name, complaint_number, new_status, category_name):
    """
    Sends an email to the student when their complaint status changes.
    """
    status_display = new_status.replace("_", " ").title()
    
    subject = f"Update on Complaint #{complaint_number} - {status_display}"
    
    message = f"""
Hello {name},

The status of your complaint has been updated.

Complaint Number: {complaint_number}
Category: {category_name}
New Status: {status_display}

You can log in to your dashboard to view more details.

Regards,
Hostel Management Centre
National Institute of Technology Patna
    """
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email],
        fail_silently=False,
    )