from django.urls import path
from .views import RegisterView, ProfileView, ProductCreateView, \
    UserServiceListView, ProductDetailView, ProductListView, ContactSupplierView, ProductDetailAllView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('partnerships/register/', RegisterView.as_view(), name='register'),  # Регистрация
    path('partnerships/profile/', ProfileView.as_view(), name='profile'),  # Profile
    path('partnerships/product-create/', ProductCreateView.as_view(), name='product-list'),  # Создание
    path('partnerships/lichnyi_kabinet/', UserServiceListView.as_view(), name='list-for-company'),  # лич каб
    path('partnerships/login/', obtain_auth_token, name='login'),
    path('partnerships/lichnyi_kabinet/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    # лич каб с delete update
    path('partnerships/product-list/', ProductListView.as_view(), name='product-list'),
    path('partnerships/products/detail/<int:pk>/', ProductDetailAllView.as_view(), name='product-detail'),
    path('partnerships/products/detail/<int:pk>/contact/', ContactSupplierView.as_view(), name='contact-supplier'),

]
