from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from .models import Service
from django.conf import settings
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Company, Message


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'type', 'title', 'email', 'description', 'company', 'created_at']
        read_only_fields = ['user']


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Company
        fields = ['user', 'type']

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        # Хеширование пароля перед сохранением
        user_data['password'] = make_password(user_data['password'])
        user = User.objects.create(**user_data)
        user = Company.objects.create(user=user, **validated_data)
        return user


class MessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(max_length=255, required=True)
    sender_email = serializers.EmailField(required=True)

    class Meta:
        model = Message
        fields = ['service', 'content', 'sender_name', 'sender_email']

    def create(self, validated_data):
        sender_name = validated_data.pop('sender_name')
        sender_email = validated_data.pop('sender_email')
        message = super().create(validated_data)

        # Отправка почты
        self.send_email(message.service, sender_name, sender_email, message.content)

        return message

    def send_email(self, service, sender_name, sender_email, message_content):
        subject = f'New message from {sender_name}'
        message = f'Sender Name: {sender_name}\nSender Email: {sender_email}\n\nMessage:\n{message_content}'
        recipient_list = [service.email]

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipient_list,
            fail_silently=False,
        )
