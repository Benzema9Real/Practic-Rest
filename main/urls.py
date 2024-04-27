from django.urls import path
from .views import ProductAPIView, UserRegistrationView, CommentAPIView, GradeAPIView,EditorViewSet

urlpatterns = [
    path('api/v1/product/', ProductAPIView.as_view()),
    path('api/v1/comment/', CommentAPIView.as_view()),
    path('api/v1/grade/', GradeAPIView.as_view()),
    path('api/v1/register/', UserRegistrationView.as_view()),
    path('api/v1/regiscvbbbvter/', EditorViewSet.as_view()),

]
