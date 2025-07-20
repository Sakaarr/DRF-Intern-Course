from django.urls import path
from .views import (
    EventListCreateView, EventDetailView, RegisterEventView,
    MyRegistrationsView, AdminRegistrationUpdateView
)

urlpatterns = [
    path('events/', EventListCreateView.as_view()),
    path('events/<int:pk>/', EventDetailView.as_view()),
    path('events/<int:pk>/register/', RegisterEventView.as_view()),
    path('my-registrations/', MyRegistrationsView.as_view()),
    path('admin/registrations/<int:pk>/', AdminRegistrationUpdateView.as_view()),
]
