
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("stock_market", "0005_alter_product_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="max_price",
            new_name="highPrice",
        ),
        migrations.RenameField(
            model_name="product",
            old_name="min_price",
            new_name="lastPrice",
        ),
        migrations.RenameField(
            model_name="product",
            old_name="price",
            new_name="lowPrice",
        ),
    ]
