from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from drf_spectacular.utils import extend_schema
from .models import Event, Registration
from .serializers import EventSerializer, RegistrationSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework.generics import get_object_or_404
from rest_framework import serializers
class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrReadOnly]

class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

@extend_schema(request=RegistrationSerializer, responses=RegistrationSerializer)
class RegisterEventView(generics.CreateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    # permission_classes = [permissions.IsAuthenticated]
    # parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        event = get_object_or_404(Event, pk=self.kwargs['pk'])

    # Optional: Check if user already registered for this event
        if Registration.objects.filter(user=self.request.user, event=event).exists():
            raise serializers.ValidationError("You have already registered for this event.")

        serializer.save(user=self.request.user, event=event)

class MyRegistrationsView(generics.ListAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Registration.objects.filter(user=self.request.user)

class AdminRegistrationUpdateView(generics.UpdateAPIView):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAdminUser]
