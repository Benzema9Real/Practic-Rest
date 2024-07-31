from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, SendMessageView, SentMessagesListView
from .views import UserRegistrationView,UserServiceListView,ServiceListView
router = DefaultRouter()
router.register(r'services', ServiceViewSet)

urlpatterns = [
    path('router', include(router.urls)),
    path('register/', UserRegistrationView.as_view(), name='company-register'),

    path('list-for-company/', UserServiceListView.as_view(), name='company-register'),
    path('services/', ServiceListView.as_view(), name='services-list'),
    path('send-message/', SendMessageView.as_view(), name='send-message'),
    path('sent-messages/', SentMessagesListView.as_view(), name='sent-messages'),
]




