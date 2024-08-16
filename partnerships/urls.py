from django.urls import path
from .views import RegisterView, ProfileView, ProductCreateView, \
    UserServiceListView, ProductDetailView, ProductListView, ContactSupplierView, ProductDetailAllView, \
    ProductDetailUpdateView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('partnerships/register/', RegisterView.as_view(), name='register'),  # Регистрация
    path('partnerships/profile/', ProfileView.as_view(), name='profile'),  # Profile
    path('partnerships/product-create/', ProductCreateView.as_view(), name='product-list'),  # Создание
    path('partnerships/lichnyi_kabinet/', UserServiceListView.as_view(), name='list-for-company'),  # лич каб
    path('partnerships/login/', obtain_auth_token, name='login'),
    path('partnerships/lichnyi_kabinet/edition/<int:pk>/', ProductDetailUpdateView.as_view(), name='product-detail'),
    # редакция своего product
    path('partnerships/lichnyi_kabinet/detail/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    # подробнее о моем product
    path('partnerships/product-list/', ProductListView.as_view(), name='product-list'),  # общий лист
    path('partnerships/products-list/detail/<int:pk>/', ProductDetailAllView.as_view(), name='product-detail'),
    # общий детейл
    path('partnerships/products-list/detail/<int:pk>/contact/', ContactSupplierView.as_view(), name='contact-supplier'),
    # oтправка по email

]
