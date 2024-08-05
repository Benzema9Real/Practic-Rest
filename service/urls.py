from django.urls import path
from .views import ServiceView, MessageCreateView
from .views import UserRegistrationView, UserServiceListView, ServiceListView

urlpatterns = [

    path('register/', UserRegistrationView.as_view(), name='company-register'),  # Регистрация
    path('ServiceView/', ServiceView.as_view(), name='service-create'),  # Создание услуг
    path('list-for-company/', UserServiceListView.as_view(), name='company-list'),  # Личный каб
    path('services/', ServiceListView.as_view(), name='services-list'),  # Общий List
    path('send-message/', MessageCreateView.as_view(), name='message-create'),  # Отправка email
]
