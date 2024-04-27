# Generated by Django 5.0.4 on 2024-04-23 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Filter',
        ),
        migrations.AddField(
            model_name='avatar',
            name='role',
            field=models.CharField(blank=True, max_length=200, verbose_name='Роль'),
        ),
    ]
