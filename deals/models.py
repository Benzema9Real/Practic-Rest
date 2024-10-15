from django.db import models
from django.contrib.auth.models import User
from .validators import validate_pdf_file, validate_file_size, validate_non_negative
import base64

class DealsSector(models.Model):
    ru = models.CharField('Название сектора (русский)', max_length=100)
    en = models.CharField('Название сектора (английский)', max_length=100)

    def __str__(self):
        return self.ru


class Country(models.Model):
    name_ru = models.CharField('Страна (русский)', max_length=100)
    name_en = models.CharField('Страна (английский)', max_length=100)

    def __str__(self):
        return self.name_ru


class PaymentCondition(models.Model):
    name_ru = models.CharField('Условия оплаты (русский)', max_length=50)
    name_en = models.CharField('Условия оплаты (английский)', max_length=50)

    def __str__(self):
        return self.name_ru




class Deals(models.Model):
    company_name = models.CharField('Название компании', max_length=255)
    delivers_self = models.BooleanField('Доставляете сами', default=False)
    economic_sectors = models.ManyToManyField(DealsSector, blank=True)  # связь ManyToMany с новой моделью
    com_offer = models.FileField('Коммерческое предложение', upload_to='deals/offers/', blank=True, null=True,
                                 validators=[validate_file_size, validate_pdf_file])
    product_photo = models.ImageField('Фото товара', upload_to='deals/product_photos/', blank=True, null=True)
    video_presentation = models.URLField('Видео презентация', blank=True, null=True)
    website_url = models.URLField('Ссылка на сайт', blank=True, null=True)
    what_do_you_offer = models.CharField('Что предлагаете', max_length=400)  # не более 400 символов
    price = models.PositiveIntegerField('Стоимость', validators=[validate_non_negative])  # integer вместо Decimal
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activate = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='deals')
    location = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Местоположение")
    payment_condition = models.ForeignKey(PaymentCondition, on_delete=models.SET_NULL, null=True, verbose_name='Условия оплаты')
    contact_email = models.EmailField('Почта для связи', blank=True, null=True)

    def __str__(self):
        return self.company_name


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.CharField(max_length=1000)


class FavoriteDeals(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites_deals')
    deal = models.ForeignKey(Deals, on_delete=models.CASCADE, related_name='favorited_by_deals')

    class Meta:
        unique_together = ('user', 'deal')

    def __str__(self):
        return f"{self.user.username} - {self.deal.company_name}"
