from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiExample
from drf_spectacular.utils import extend_schema_view, extend_schema, OpenApiExample
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers,permissions
from .models import Event, Registration
from .serializers import EventSerializer, EventDetailSerializer, RegistrationSerializer
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['start_date', 'location']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EventDetailSerializer
        return super().get_serializer_class()

    @extend_schema(
        summary="Event summary",
        description="Get summary of registrations for an event",
        responses={
            200: serializers.SerializerMethodField(),
        }
    )
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        event = self.get_object()
        registrations = event.registrations.all()
        summary = {
            'total_applied': registrations.filter(status='applied').count(),
            'total_approved': registrations.filter(status='approved').count(),
            'total_declined': registrations.filter(status='declined').count(),
            'remaining_seats': event.capacity - event.total_registered
        }
        return Response(summary)

    @extend_schema(
        summary="Register for an event",
        description="Register an authenticated user for an event",
        request=RegistrationSerializer,
        responses={
            201: RegistrationSerializer,
            400: serializers.SerializerMethodField()
        },
        examples=[
            OpenApiExample(
                'Valid registration',
                value={
                    'event_id': '550e8400-e29b-41d4-a716-446655440000',
                    'payment_screenshot': 'data:image/png;base64,...'
                }
            )
        ]
    )
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def register(self, request, pk=None):
        event = self.get_object()
        serializer = RegistrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Registration.objects.all()
        return Registration.objects.filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update']:
            return [IsAuthenticated]
        return super().get_permissions()

# Admin Registration View
class AdminRegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'event']