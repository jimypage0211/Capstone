# Generated by Django 5.0 on 2024-02-01 04:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0019_alter_restaurant_imgurl'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurant',
            old_name='imgURL',
            new_name='img_URL',
        ),
    ]