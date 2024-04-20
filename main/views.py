from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from .models import Product, Comment, Grade
from .permissions import IsEditor
from .serializers import AvatarSerializer, ProductImageSerializer, CommentSerializer, GradeSerializer


class ProductAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductImageSerializer
    authentication_classes = []
    permission_classes = []

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data = {
                "user_id": user.id,
                "message": "User registered successfully."
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = []
    permission_classes = []

class GradeAPIView(generics.ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    authentication_classes = []
    permission_classes = []