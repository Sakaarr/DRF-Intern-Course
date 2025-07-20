from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Event, UserRegistration
from .serializers import EventSerializer, UserRegistrationSerializer
# from .permissions import IsAdminOrReadOnly
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(description='List all events'),
    create=extend_schema(description='Create a new event'),
    retrieve=extend_schema(description='Get event details'),
    update=extend_schema(description='Update event'),
    destroy=extend_schema(description='Delete event'),
)
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    # permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=['get'])
    def registrations(self, request, pk=None):
        event = self.get_object()
        registrations = event.userregistration_set.all()
        serializer = UserRegistrationSerializer(registrations, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(description='List registrations'),
    create=extend_schema(description='Register for event'),
)
class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = UserRegistration.objects.all()
    serializer_class = UserRegistrationSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

