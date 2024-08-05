from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .serializers import CompanySerializer, MessageSerializer, ServiceSerializer
from .permissions import IsCompany
from .models import Service, Message
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from .permissions import IsPerson


 # Создание услуги
class ServiceView(generics.CreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.groups.filter(name='Company').exists():
            return Service.objects.filter(user=self.request.user)
        return Service.objects.all()


class UserRegistrationView(generics.CreateAPIView):  # регистрация
    queryset = User.objects.all()
    serializer_class = CompanySerializer
    permission_classes = []

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserServiceListView(generics.ListAPIView):   # Личный кабинет
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompany]

    def get_queryset(self):
        return Service.objects.filter(user=self.request.user)


class ServiceListView(generics.ListAPIView):  # Общий лист услуг
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsPerson]

    def get_queryset(self):
        return Service.objects.filter(activate=True)


class MessageCreateView(generics.CreateAPIView):  # Отправка по email
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
