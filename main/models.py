from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Product(models.Model):
    name = models.CharField('Название', max_length=100)
    category = models.CharField('Категория',max_length=100)
    summary = models.CharField('краткое описание', max_length=100)
    full_content = models.TextField('полное описание')
    price = models.FloatField('цена')
    quantity = models.IntegerField('количество на складе')

    def __str__(self):
        return self.name

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    my_image = models.ImageField(upload_to='images/', blank=True)


class Comment(models.Model):
    comment = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment')
    my_comment = models.TextField('Комментарий')



class Grade(models.Model):
    grade = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='grade')
    my_grade = models.IntegerField('оценка от 1 до 5', validators=[MaxValueValidator(5),MinValueValidator(1)])

class Avatar(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='avatar')
    role = models.CharField('Роль',max_length=200, blank=True)
    address = models.CharField('Адрес', max_length=100, blank=True)
    country = models.CharField('Страна', max_length=100, blank=True)
    region = models.CharField('Область', max_length=100, blank=True)
    place_of_birth = models.CharField('Место рождения', max_length=200, blank=True)



