from django.contrib.auth.hashers import make_password
from .models import User
from rest_framework import serializers

from .models import Product, Avatar, ProductImage


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = ProductImage
        fields = ['image', 'my_image','product']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}  # Убедитесь, что пароль


class AvatarSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Avatar
        fields = ['user', 'address', 'country', 'region', 'place_of_birth']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        # Хеширование пароля перед сохранением
        user_data['password'] = make_password(user_data['password'])
        user = User.objects.create(**user_data)
        avatar = Avatar.objects.create(user=user, **validated_data)
        return avatar
