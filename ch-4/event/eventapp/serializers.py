from rest_framework import serializers
from .models import Event, Registration
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['total_registered']

class RegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event_title = serializers.ReadOnlyField(source='event.title')

    class Meta:
        model = Registration
        fields = ['id', 'user', 'event', 'event_title', 'status', 'payment_screenshot', 'registered_at']
        read_only_fields = ['id', 'user', 'status', 'registered_at']
