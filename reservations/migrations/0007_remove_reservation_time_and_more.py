# Generated by Django 5.0 on 2024-01-31 17:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0006_shift'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='time',
        ),
        migrations.RemoveField(
            model_name='restaurant',
            name='reserverdTables',
        ),
        migrations.RemoveField(
            model_name='shift',
            name='end',
        ),
        migrations.RemoveField(
            model_name='shift',
            name='start',
        ),
        migrations.AddField(
            model_name='reservation',
            name='shift',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='reservations.shift'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='shift',
            name='shift',
            field=models.CharField(choices=[('10AM - 12PM', 'First'), ('12PM - 2PM', 'Second'), ('2PM - 4PM', 'Third'), ('4PM - 6PM', 'Fourth'), ('6PM - 8PM', 'Fifth'), ('8PM - 10PM', 'Sixth'), ('10PM - 12AM', 'Seventh')], max_length=11, null=True),
        ),
    ]
