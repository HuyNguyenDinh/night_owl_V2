# Generated by Django 4.1 on 2022-12-22 07:57

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0009_remove_voucher_percentage_voucher_constraint_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='voucher',
            name='percentage_voucher_constraint',
        ),
        migrations.AddConstraint(
            model_name='voucher',
            constraint=models.CheckConstraint(check=models.Q(('is_percentage', False), models.Q(('is_percentage', True), ('discount__lte', Decimal('100'))), _connector='OR'), name='percentage_voucher_constraint'),
        ),
    ]
