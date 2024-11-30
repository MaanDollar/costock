# Generated by Django 5.1.3 on 2024-11-29 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stock", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="owned",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name="recommended",
            name="price",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
