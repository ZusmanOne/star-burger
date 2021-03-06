# Generated by Django 3.2 on 2022-05-06 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0052_order_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='called_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата Звонка'),
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Дата Доставки'),
        ),
        migrations.AddField(
            model_name='order',
            name='registered_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True, null=True, verbose_name='Дата создания'),
        ),
    ]
