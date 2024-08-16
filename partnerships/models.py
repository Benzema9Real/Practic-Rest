import secrets
from django.db import models
from django.contrib.auth.models import User, Group

class Product(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    transport_included = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sale_period = models.IntegerField()  # Продолжительность продажи в днях
    activate = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name
class Profile(models.Model):
    ROLE_CHOICES = [
        ('supplier', 'Supplier'),
        ('buyer', 'Buyer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='none')
    business_name = models.CharField(max_length=100, blank=True, null=True)
    business_description = models.TextField(blank=True, null=True)
    business_website = models.URLField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk is None:
            if self.role == 'supplier':
                group = Group.objects.get(name='Supplier')
            else:
                group = Group.objects.get(name='Buyer')
            self.user.groups.add(group)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.role
