from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import Service
from django.conf import settings
from rest_framework import serializers
from .models import Profile, Type, Contact


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['business_name', 'business_description', 'business_website']
        ref_name = 'ProfileSerializerService'
        read_only_fields = ['user']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        ref_name = 'UserSerializerService'
        extra_kwargs = {'password': {'write_only': True}}


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'type', 'email', 'price', 'created_at', 'updated_at']
        read_only_fields = ['user']
        ref_name = 'ServiceSerializerService'


class ServiceAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'type', 'email', 'price', 'created_at', 'updated_at']
        ref_name = 'ServiceAllSerializerService'


class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=Profile.CHOICE, write_only=True)
    business_name = serializers.CharField(required=False, allow_blank=True)
    business_description = serializers.CharField(required=False, allow_blank=True)
    business_website = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'business_name', 'business_description', 'business_website'
                  ]
        extra_kwargs = {'password': {'write_only': True}}
        ref_name = 'ServiceRegisterSerializer'

    def create(self, validated_data):
        role = validated_data.pop('role')
        business_name = validated_data.pop('business_name', '')
        business_description = validated_data.pop('business_description', '')
        business_website = validated_data.pop('business_website', '')

        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user, role=role, business_name=business_name,
                               business_description=business_description, business_website=business_website,
                               )
        return user


class ContactSupplierSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField()
    message = serializers.CharField(max_length=1000)
    class Meta:
        model = Contact
        fields = '__all__'
        ref_name = 'ContactSerializerService'
