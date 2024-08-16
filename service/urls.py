from django.urls import path
from .views import UserRegistrationView, UserServiceListView, ServiceListView,ServiceCreateView, MessageCreateView

urlpatterns = [
    path('service/register/', UserRegistrationView.as_view(), name='company-register'),  # Регистрация
    path('service/servicecreate/', ServiceCreateView.as_view() ,name='service-create'),  # Создание услуг
    path('service/list-for-company/', UserServiceListView.as_view(), name='company-list'),  # Личный каб
    path('service/services/', ServiceListView.as_view(), name='services-list'),  # Общий List
    path('service/send-message/', MessageCreateView.as_view(), name='message-create'),  # Отправка email
]
