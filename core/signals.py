from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Complaint, StatusLog


@receiver(pre_save, sender=Complaint)
def log_status_change(sender, instance, **kwargs):
    # Skip new objects (creation handled elsewhere)
    if not instance.pk:
        return

    try:
        old_instance = Complaint.objects.get(pk=instance.pk)
    except Complaint.DoesNotExist:
        return

    # Only act on real status changes
    if instance.status != old_instance.status:
        # 🔽 Read admin remark if provided by view
        message = getattr(
            instance,
            "_status_change_message",
            f"Status changed from {old_instance.status} to {instance.status}"
        )

        StatusLog.objects.create(
            complaint=instance,
            status=instance.status,
            message=message
        )
