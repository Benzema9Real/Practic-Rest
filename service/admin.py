from django.contrib import admin
from .models import Company, Service, Type, Message

admin.site.register(Company)
admin.site.register(Service)
admin.site.register(Type)
admin.site.register(Message)
