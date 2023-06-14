# Generated by Django 4.2.2 on 2023-06-13 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gryb_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(default='Самовывоз с. Алматы', max_length=255, verbose_name='Адрес доставки'),
        ),
        migrations.AddField(
            model_name='order',
            name='recipient_email',
            field=models.EmailField(default='Null', max_length=254, verbose_name='Email получателя'),
        ),
        migrations.AddField(
            model_name='order',
            name='recipient_phone',
            field=models.CharField(default='Null', max_length=20, verbose_name='Номер телефона получателя'),
        ),
        migrations.AlterField(
            model_name='order',
            name='recipient_name',
            field=models.CharField(default='Null', max_length=255, verbose_name='Имя получателя'),
        ),
    ]
