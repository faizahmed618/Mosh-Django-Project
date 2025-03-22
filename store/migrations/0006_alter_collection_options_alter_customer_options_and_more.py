# Generated by Django 4.2.17 on 2025-03-22 13:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0005_rename_last_updated_product_last_update"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="collection",
            options={"ordering": ["title"]},
        ),
        migrations.AlterModelOptions(
            name="customer",
            options={"ordering": ["first_name", "last_name"]},
        ),
        migrations.AlterModelOptions(
            name="product",
            options={"ordering": ["title"]},
        ),
        migrations.AlterField(
            model_name="product",
            name="unit_price",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=6,
                validators=[django.core.validators.MinValueValidator(1)],
            ),
        ),
    ]
