from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ServiceSerializer, ProfileSerializer, RegisterSerializer, ServiceAllSerializer, \
    ContactSupplierSerializer
from .permissions import IsCompany, IsPerson
from .models import Service, Profile
from rest_framework import status, generics, permissions


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


class ServiceCreateView(generics.CreateAPIView):  # Создание
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated, IsCompany]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.groups.filter(name='Company').exists():
            return Service.objects.filter(user=self.request.user)
        return Service.objects.all()


class ServiceDetailUpdateView(generics.RetrieveUpdateDestroyAPIView):  # Личный кабинет
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsCompany, IsAuthenticated]

    def get_queryset(self):
        return Service.objects.filter(user=self.request.user)


class ServiceDetailView(generics.RetrieveAPIView):  # Личный кабинет
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [IsCompany, IsAuthenticated]

    def get_queryset(self):
        return Service.objects.filter(user=self.request.user)


class ServiceDetailAllView(generics.RetrieveAPIView):  # Detail
    queryset = Service.objects.filter(activate=True)
    serializer_class = ServiceAllSerializer
    permission_classes = [IsAuthenticated]


class ContactSupplierView(APIView):
    serializer_class = ContactSupplierSerializer
    permission_classes = [IsAuthenticated, IsPerson]

    def post(self, request, pk):
        try:
            service = Service.objects.get(pk=pk, activate=True)
        except Service.DoesNotExist:
            return Response({"error": "Product not found or not activated"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ContactSupplierSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            email = serializer.validated_data['email']
            message = serializer.validated_data['message']

            subject = f"New inquiry for your product: {service.name}"
            full_message = f"You have received a new inquiry from {name} ({email}):\n\n{message}"

            send_mail(subject, full_message, email, [service.email])

            return Response({"success": "Message sent successfully"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserServiceListView(generics.ListAPIView):  # Личный кабинет
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompany]

    def get_queryset(self):
        return Service.objects.filter(user=self.request.user)


class ServiceListView(generics.ListAPIView):
    queryset = Service.objects.filter(activate=True)
    serializer_class = ServiceAllSerializer
    permission_classes = [IsAuthenticated]
