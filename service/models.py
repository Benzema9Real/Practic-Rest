from django.db import models
from django.contrib.auth.models import User, Group


class Type(models.Model):
    name_type = models.CharField('Название типа', max_length=340)

    def __str__(self):
        return self.name_type


class Service(models.Model):
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='type')
    name = models.CharField('Название услуги', max_length=255)
    description = models.TextField('Описание')
    email = models.EmailField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activate = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    CHOICE = [
        ('company', 'Я подрядчик '),
        ('man', 'Я заказчик')
    ]
    role = models.CharField(max_length=300, choices=CHOICE)
    business_name = models.CharField(max_length=100, blank=True, null=True)
    business_description = models.TextField(blank=True, null=True)
    business_website = models.URLField(blank=True, null=True)
    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.role == 'company':
                group = Group.objects.get(name='Company')
            else:
                group = Group.objects.get(name='Person')
            self.user.groups.add(group)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.role


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.CharField(max_length=1000)

