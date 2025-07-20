
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Registration
@receiver(post_save, sender=Registration)
def update_total_registered(sender, instance, **kwargs):
    if instance.status == 'approved':
        instance.event.total_registered = instance.event.registrations.filter(status='approved').count()
        instance.event.save()
