from django.db import models
import uuid

class Event(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='upcoming')
    is_active = models.BooleanField(default=True)
    banner = models.ImageField(upload_to='event_banners/', null=True, blank=True)
    total_registrations = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class UserRegistration(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
        ('refunded', 'Refunded'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    screenshot = models.ImageField(upload_to='screenshots/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='applied')
    token = models.CharField(max_length=12, unique=True, editable=False)
    registered_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = uuid.uuid4().hex[:12].upper()

        # Adjust total_registrations only when status changes to approved
        if self.pk:
            original = UserRegistration.objects.get(pk=self.pk)
            if original.status != 'approved' and self.status == 'approved':
                self.event.total_registrations += 1
                self.event.save()
            elif original.status == 'approved' and self.status != 'approved':
                self.event.total_registrations = max(0, self.event.total_registrations - 1)
                self.event.save()
        else:
            if self.status == 'approved':
                self.event.total_registrations += 1
                self.event.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.event.title}"