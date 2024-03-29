# Generated by Django 5.0 on 2024-01-27 18:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0005_rename_maxtables_restaurant_personcapacity_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('personCapacity', models.IntegerField(editable=False)),
                ('tablesCapacity', models.IntegerField(editable=False)),
                ('reserverdTables', models.IntegerField(editable=False)),
                ('isFull', models.BooleanField(default=False, editable=False)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shifts', to='reservations.restaurant')),
            ],
        ),
    ]
