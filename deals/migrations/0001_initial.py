# Generated by Django 5.0.2 on 2024-10-08 11:31

import deals.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_ru', models.CharField(max_length=100, verbose_name='Страна (русский)')),
                ('name_en', models.CharField(max_length=100, verbose_name='Страна (английский)')),
            ],
        ),
        migrations.CreateModel(
            name='DealsSector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ru', models.CharField(max_length=100, verbose_name='Название сектора (русский)')),
                ('en', models.CharField(max_length=100, verbose_name='Название сектора (английский)')),
            ],
        ),
        migrations.CreateModel(
            name='Deals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255, verbose_name='Название компании')),
                ('delivers_self', models.BooleanField(default=False, verbose_name='Доставляете сами')),
                ('com_offer', models.FileField(blank=True, null=True, upload_to='deals/offers/', validators=[deals.validators.validate_file_size, deals.validators.validate_pdf_file], verbose_name='Коммерческое предложение')),
                ('product_photo', models.ImageField(blank=True, null=True, upload_to='deals/product_photos/', verbose_name='Фото товара')),
                ('video_presentation', models.URLField(blank=True, null=True, verbose_name='Видео презентация')),
                ('website_url', models.URLField(blank=True, null=True, verbose_name='Ссылка на сайт')),
                ('what_do_you_offer', models.CharField(max_length=400, verbose_name='Что предлагаете')),
                ('price', models.PositiveIntegerField(validators=[deals.validators.validate_non_negative], verbose_name='Стоимость')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('activate', models.BooleanField(default=False)),
                ('payment_condition', models.CharField(choices=[('prepayment', 'Предоплата'), ('postpayment', 'Постоплата'), ('credit', 'Кредит')], default='prepayment', verbose_name='Условия оплаты')),
                ('contact_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Почта для связи')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='deals.country', verbose_name='Местоположение')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deals', to=settings.AUTH_USER_MODEL)),
                ('economic_sectors', models.ManyToManyField(blank=True, to='deals.dealssector')),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteDeals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorited_by_deals', to='deals.deals')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites_deals', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'deal')},
            },
        ),
    ]
