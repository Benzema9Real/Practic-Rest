from django.contrib.auth.models import User
from rest_framework import viewsets
from .serializers import CompanySerializer, MessageSerializer
from .permissions import IsCompany
from rest_framework import generics, permissions
from .models import Service, Message
from .serializers import ServiceSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.mail import send_mail
from .permissions import IsPerson
from django.conf import settings

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), IsCompany()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.groups.filter(name='Company').exists():
            return Service.objects.filter(user=self.request.user)
        return Service.objects.all()


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CompanySerializer
    permission_classes = []

    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserServiceListView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompany]

    def get_queryset(self):
        return Service.objects.filter(user=self.request.user)


class ServiceListView(generics.ListAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated, IsPerson]

    def get_queryset(self):
        return Service.objects.filter(activate=True)


class SendMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsPerson]

    def post(self, request, *args, **kwargs):
        service_id = request.data.get('service_id')
        content = request.data.get('content')

        try:
            service = Service.objects.get(id=service_id)

            # Создание записи в модели Message
            message = Message.objects.create(
                service=service,
                sender=request.user,
                content=content
            )

            # Отправка письма
            send_mail(
                subject=f"Message from {request.user.username}",
                message=content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[service.email],
                fail_silently=False,
            )

            return Response({'detail': 'Message sent successfully'}, status=status.HTTP_200_OK)
        except Service.DoesNotExist:
            return Response({'detail': 'Service not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SentMessagesListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsPerson]

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user)