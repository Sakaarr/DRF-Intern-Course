from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, UserRegistrationViewSet

router = DefaultRouter()
router.register('events', EventViewSet)
router.register('registrations', UserRegistrationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
