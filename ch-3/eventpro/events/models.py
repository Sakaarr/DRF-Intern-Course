from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=200)
    capacity = models.IntegerField()
    total_registered = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Registration(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('approved', 'Approved'),
        ('declined', 'Declined'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    payment_screenshot = models.ImageField(upload_to='payments/',null=True, blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
