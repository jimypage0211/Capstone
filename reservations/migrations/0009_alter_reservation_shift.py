# Generated by Django 5.0 on 2024-01-31 17:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0008_alter_shift_shift'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='shift',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='reservations.shift'),
        ),
    ]