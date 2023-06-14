# Generated by Django 4.2.2 on 2023-06-14 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gryb_app', '0004_carouselimage_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='carouselimage',
            name='button_text',
            field=models.CharField(blank=True, max_length=255, verbose_name='Текст на кнопке'),
        ),
        migrations.AlterField(
            model_name='carouselimage',
            name='text',
            field=models.CharField(blank=True, max_length=255, verbose_name='Текст на слайде'),
        ),
    ]
