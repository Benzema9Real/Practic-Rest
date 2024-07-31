from django.db import models
from django.contrib.auth.models import User,Group

class Type(models.Model):
    name_type = models.CharField('Название типа', max_length=340)

    def __str__(self):
        return self.name_type

class Service(models.Model):
    type = models.OneToOneField(Type, on_delete=models.CASCADE, related_name='type')
    title = models.CharField('Название услуги', max_length=255)
    description = models.TextField('Описание')
    email = models.EmailField()
    company = models.CharField('Название компании', max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    activate = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return self.title

class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    CHOICE = [
        ('company', 'Я бизнесмен, который предоставляет услуги'),
        ('man', 'Я бизнесмен, который ищу бизнес услуги')
    ]
    type = models.CharField(max_length=300, choices=CHOICE)

    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.type == 'company':
                group = Group.objects.get(name='Company')
            else:
                group = Group.objects.get(name='Person')
            self.user.groups.add(group)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.type


class Message(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField('Message Content')
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.service.company}"
