# Generated by Django 5.0 on 2024-01-31 17:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0011_remove_reservation_shift'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='shift',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='reservations.shift'),
            preserve_default=False,
        ),
    ]
