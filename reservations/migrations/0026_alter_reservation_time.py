# Generated by Django 5.0 on 2024-02-12 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0025_rename_when_reserved_reservation_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='time',
            field=models.TimeField(),
        ),
    ]
