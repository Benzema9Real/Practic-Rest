from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework import generics, serializers, status, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegisterSerializer, ProfileSerializer, ProductSerializer, \
    ProductAllSerializer, ContactSupplierSerializer
from .models import Profile, Product, Message
from .permissions import IsSupplier, IsBuyer


class RegisterView(generics.CreateAPIView):  # Регистрация
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = []


class ProfileView(generics.RetrieveUpdateAPIView):  # Профиль
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return self.request.user.profile


class ProductCreateView(generics.CreateAPIView):  # Создание
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.groups.filter(name='Supplier').exists():
            return Product.objects.filter(user=self.request.user)
        return Product.objects.all()


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):  # Личный кабинет
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsSupplier, IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)


class ProductDetailAllView(generics.RetrieveAPIView):  # Detail
    queryset = Product.objects.filter(activate=True)
    serializer_class = ProductAllSerializer
    permission_classes = [IsAuthenticated]


class ContactSupplierView(APIView):
    serializer_class = ContactSupplierSerializer
    def post(self, request, pk):
        try:
            product = Product.objects.get(pk=pk, activate=True)
        except Product.DoesNotExist:
            return Response({"error": "Product not found or not activated"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ContactSupplierSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            message = serializer.validated_data['message']

            subject = f"New inquiry for your product: {product.name}"
            full_message = f"You have received a new inquiry from {name} ({email}):\n\n{message}"

            send_mail(subject, full_message, email, [product.email])

            return Response({"success": "Message sent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserServiceListView(generics.ListAPIView):  # Личный кабинет
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsSupplier]

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user)


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(activate=True)
    serializer_class = ProductAllSerializer
    permission_classes = [IsAuthenticated]
