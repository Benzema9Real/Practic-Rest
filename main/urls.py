from django.urls import path
from .views import ProductAPIView, UserRegistrationView

urlpatterns = [
    path('api/v1/thingslist1/', ProductAPIView.as_view()),
path('api/v1/register/', UserRegistrationView.as_view()),

]
