# Generated by Django 4.1 on 2023-01-03 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0011_alter_address_note_alter_rating_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={},
        ),
        migrations.AlterField(
            model_name='user',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.01, max_digits=20),
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.CheckConstraint(check=models.Q(('balance__gte', 0)), name='min_user_balance'),
        ),
    ]
