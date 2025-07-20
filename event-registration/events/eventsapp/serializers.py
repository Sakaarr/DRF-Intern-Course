from rest_framework import serializers
from .models import Event, UserRegistration
from django.core.mail import send_mail
from django.conf import settings

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_registrations']
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRegistration
        read_only_fields = ['id', 'registered_at', 'token']
        fields = '__all__'

    def validate(self, attrs):
        event = attrs.get('event') or getattr(self.instance, 'event', None)
        status = attrs.get('status', getattr(self.instance, 'status', 'applied'))
        if status == 'approved' and event.total_registrations >= event.capacity:
            raise serializers.ValidationError("Event capacity reached.")
        return attrs

    def create(self, validated_data):
        registration = super().create(validated_data)
        event = registration.event
        if registration.status == 'approved':
            event.total_registrations += 1
            event.save()
        send_mail(
            subject='Event Registration Confirmation',
            message=f"Thanks for registering for {event.title}. Your token: {registration.token}",
            from_email='noreply@example.com',
            recipient_list=[registration.email],
            fail_silently=True,
        )
        return registration
