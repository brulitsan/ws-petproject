
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("stock_market", "0006_rename_max_price_product_highprice_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product",
            old_name="name",
            new_name="symbol",
        ),
    ]
