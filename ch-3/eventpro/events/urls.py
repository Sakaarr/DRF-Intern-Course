from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, RegistrationViewSet, AdminRegistrationViewSet

router = DefaultRouter()
router.register(r'events', EventViewSet,basename='event')
router.register(r'registrations', RegistrationViewSet,basename='registration')
router.register(r'admin/registrations', AdminRegistrationViewSet,basename='admin-registration')

urlpatterns = [
    path('', include(router.urls)),
]
