from django.urls import path
from .views import (
    DealsCreateView,
    UserDealsListView,
    DealsDetailView,
    DealsListView,
    DealsDetailAllView,
    DealsDetailUpdateView,
    AddFavoriteDealsView,
    RemoveFavoriteDealsView,
    FavoriteDealsListView,
    ContactSupplierView,
    DealsPaymentConditionListView,
    DealsSectorListView, DealsCountryListView,
)

urlpatterns = [

    path('deals/product-create/', DealsCreateView.as_view(), name='product-list'),  # Создание
    path('deals/country-list/', DealsCountryListView.as_view(), name='product-list'),  # Создание
    path('deals/payment-conditions/', DealsPaymentConditionListView.as_view(), name='payment-conditions'),
    path('deals/economic-sectors/', DealsSectorListView.as_view(), name='deals-economic-sectors'),
    path('deals/favorites/add/<int:pk>/', AddFavoriteDealsView.as_view(), name='add-favorite_deals'),
    path('deals/favorites/remove/<int:pk>/', RemoveFavoriteDealsView.as_view(), name='remove-favorite_deals'),
    path('deals/favorites/', FavoriteDealsListView.as_view(), name='favorite-list_deals'),
    path('deals/lichnyi_kabinet/', UserDealsListView.as_view(), name='list-for-company'),  # лич каб

    path('deals/lichnyi_kabinet/edition/<int:pk>/', DealsDetailUpdateView.as_view(), name='product-detail'),
    # редакция своего product
    path('deals/lichnyi_kabinet/detail/<int:pk>/', DealsDetailView.as_view(), name='product-detail'),
    # подробнее о моем product
    path('deals/product-list/', DealsListView.as_view(), name='product-list'),  # общий лист
    path('deals/products-list/detail/<int:pk>/', DealsDetailAllView.as_view(), name='product-detail'),
    # общий детейл
    path('deals/products-list/detail/<int:pk>/contact/', ContactSupplierView.as_view(), name='contact-supplier'),
    # oтправка по email

]
