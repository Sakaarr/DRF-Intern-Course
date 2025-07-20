from rest_framework import serializers
from .models import Event, Registration
from django.contrib.auth.models import User
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'start_date', 'end_date', 'location', 'capacity', 'total_registered']
        
        
class RegistrationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    event = EventSerializer(read_only=True)
    event_id = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all(), source='event', write_only=True)

    class Meta:
        model = Registration
        fields = ['id', 'user', 'event', 'event_id', 'status', 'payment_screenshot', 'registered_at']

    def validate(self, data):
        event = data['event']
        user = self.context['request'].user
        
        # Check if event is in the past
        if event.start_date < timezone.now().date():
            raise serializers.ValidationError("Cannot register for past events")
        
        # Check if event is full
        if event.total_registered >= event.capacity:
            raise serializers.ValidationError("Event is full")
        
        # Check if user already registered
        if Registration.objects.filter(user=user, event=event).exists():
            raise serializers.ValidationError("User already registered for this event")
        
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class EventDetailSerializer(EventSerializer):
    registrations = RegistrationSerializer(many=True, read_only=True)
    
    class Meta(EventSerializer.Meta):
        fields = EventSerializer.Meta.fields + ['registrations']
