
import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ProductCategories",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "name",
                    models.CharField(
                        choices=[
                            ("криптовалюта", "криптовалюта"),
                            ("акции", "акции"),
                            ("фьючерсы", "фьючерсы"),
                            ("облигации", "облигации"),
                        ],
                        max_length=30,
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="stock_market.productcategories",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("max_price", models.DecimalField(decimal_places=3, max_digits=10)),
                ("min_price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "name",
                    models.ForeignKey(
                        default="",
                        on_delete=django.db.models.deletion.PROTECT,
                        to="stock_market.productcategories",
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "transaction_price",
                    models.DecimalField(decimal_places=3, max_digits=10),
                ),
                ("quantity", models.DecimalField(decimal_places=4, max_digits=10)),
                (
                    "type",
                    models.CharField(
                        choices=[("Покупка", "Покупка"), ("Продажа", "Продажа")],
                        max_length=30,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "product_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="stock_market.product",
                    ),
                ),
            ],
        ),
    ]
