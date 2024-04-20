from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Product, Avatar, ProductImage, Comment, Grade


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['my_grade']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['my_comment']
class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = ['my_image']

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    grade = serializers.PrimaryKeyRelatedField(queryset=Grade.objects.all())
    comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all())
    class Meta:
        model = Product
        fields = ['name','category','summary','full_content','price','quantity','image_url','comment','grade']

    def get_image_url(self, obj):
        product_image = obj.images.first()  # Получаем первое изображение товара
        return product_image.my_image.url if product_image else None
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





class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['product', 'grade']
