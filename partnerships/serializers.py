from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile, Product


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['business_name', 'business_description', 'business_website']
        ref_name = 'ProfileSerializerPartnership'
        read_only_fields = ['user']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        ref_name = 'UserSerializerPartnership'
        extra_kwargs = {'password': {'write_only': True}}


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'email', 'price', 'quantity', 'transport_included', 'created_at',
                  'updated_at', 'sale_period']
        read_only_fields = ['user']


class ProductAllSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'email', 'price', 'quantity', 'transport_included', 'created_at',
                  'updated_at', 'sale_period']


class RegisterSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=Profile.ROLE_CHOICES, write_only=True)
    business_name = serializers.CharField(required=False, allow_blank=True)
    business_description = serializers.CharField(required=False, allow_blank=True)
    business_website = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'business_name', 'business_description', 'business_website'
                  ]
        extra_kwargs = {'password': {'write_only': True}}
        ref_name = 'PartnershipsRegisterSerializer'

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
