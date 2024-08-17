from django.urls import path
from .views import RegisterView, ProfileView, ServiceCreateView, UserServiceListView, ServiceDetailUpdateView, \
    ServiceDetailView, ServiceListView, ServiceDetailAllView, ContactSupplierView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('service/register/', RegisterView.as_view(), name='register'),  # Регистрация
    path('service/profile/', ProfileView.as_view(), name='profile'),  # Profile
    path('service/service-create/', ServiceCreateView.as_view(), name='service-list'),  # Создание
    path('service/lichnyi_kabinet/', UserServiceListView.as_view(), name='list-for-company'),  # лич каб
    path('service/login/', obtain_auth_token, name='login'),
    path('service/lichnyi_kabinet/edition/<int:pk>/', ServiceDetailUpdateView.as_view(), name='service-detail'),
    # редакция своего product
    path('service/lichnyi_kabinet/detail/<int:pk>/', ServiceDetailView.as_view(), name='service-detail'),
    # подробнее о моем product
    path('service/service-list/', ServiceListView.as_view(), name='product-list'),  # общий лист
    path('service/service-list/detail/<int:pk>/', ServiceDetailAllView.as_view(), name='service-detail'),
    # общий детейл
    path('service/service-list/detail/<int:pk>/contact/', ContactSupplierView.as_view(), name='contact-supplier'),
    # oтправка по email

]
