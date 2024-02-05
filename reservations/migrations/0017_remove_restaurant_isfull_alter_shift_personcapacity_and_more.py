# Generated by Django 5.0 on 2024-01-31 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0016_alter_shift_personcapacity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restaurant',
            name='isFull',
        ),
        migrations.AlterField(
            model_name='shift',
            name='personCapacity',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='shift',
            name='tablesCapacity',
            field=models.IntegerField(default=-1),
        ),
    ]