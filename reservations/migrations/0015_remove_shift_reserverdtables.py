# Generated by Django 5.0 on 2024-01-31 18:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0014_alter_shift_shiftrange'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shift',
            name='reserverdTables',
        ),
    ]
