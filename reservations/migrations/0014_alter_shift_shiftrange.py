# Generated by Django 5.0 on 2024-01-31 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0013_rename_shift_shift_shiftrange'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shift',
            name='shiftRange',
            field=models.CharField(max_length=11),
        ),
    ]