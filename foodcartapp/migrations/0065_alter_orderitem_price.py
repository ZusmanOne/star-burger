# Generated by Django 3.2 on 2022-06-07 17:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0064_auto_20220607_1733'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(db_index=True, decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Общая стоимость товара'),
        ),
    ]
