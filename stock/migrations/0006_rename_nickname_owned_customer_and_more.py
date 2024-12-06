# Generated by Django 5.1.3 on 2024-12-06 06:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("stock", "0005_rename_customer_owned_nickname_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="owned",
            old_name="nickname",
            new_name="customer",
        ),
        migrations.RenameField(
            model_name="owned",
            old_name="stock",
            new_name="name",
        ),
        migrations.RenameField(
            model_name="recommended",
            old_name="nickname",
            new_name="customer",
        ),
        migrations.RenameField(
            model_name="recommended",
            old_name="stock",
            new_name="name",
        ),
    ]
