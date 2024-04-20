from django.contrib import admin

from .models import Product, ProductImage, Comment

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Comment)