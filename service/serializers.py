from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'type', 'title', 'description', 'company', 'created_at']
        read_only_fields = ['user']


from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Company, Message

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
        fields = ['user', 'type' ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')

        # Хеширование пароля перед сохранением
        user_data['password'] = make_password(user_data['password'])
        user = User.objects.create(**user_data)
        user = Company.objects.create(user=user, **validated_data)
        return user

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['sender', 'sent_at']