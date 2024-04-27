from django.contrib import admin

from .models import Product, ProductImage, Comment, Grade, Avatar

admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Comment)
admin.site.register(Grade)
admin.site.register(Avatar)
