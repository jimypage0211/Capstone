# Generated by Django 4.2.6 on 2024-01-25 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reservations", "0004_rename_tables_restaurant_reserverdtables"),
    ]

    operations = [
        migrations.RenameField(
            model_name="restaurant",
            old_name="maxTables",
            new_name="personCapacity",
        ),
        migrations.AddField(
            model_name="restaurant",
            name="tablesCapacity",
            field=models.IntegerField(default=300),
            preserve_default=False,
        ),
    ]
