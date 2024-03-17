# Generated by Django 4.2.10 on 2024-03-16 20:39

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stock_market", "0012_order_currency_price_alter_order_type_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="type",
            field=models.CharField(
                choices=[
                    ("Покупка", "Покупка"),
                    ("Продажа", "Продажа"),
                    ("Авто_Продажа", "Авто_Продажа"),
                    ("Авто_Покупка", "Авто_Покупка"),
                ],
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="id",
            field=models.UUIDField(
                default=uuid.UUID("b6a0bb4a-2618-4a68-bfbb-c71b73e76581"),
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
