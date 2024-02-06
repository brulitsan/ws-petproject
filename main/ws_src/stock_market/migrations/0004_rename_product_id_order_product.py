
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("stock_market", "0003_alter_product_id"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="product_id",
            new_name="product",
        ),
    ]
