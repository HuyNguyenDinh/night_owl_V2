# Generated by Django 4.1 on 2022-12-14 03:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0003_product_sold_amount_positive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='sold_amount',
            field=models.BigIntegerField(default=0),
        ),
    ]
