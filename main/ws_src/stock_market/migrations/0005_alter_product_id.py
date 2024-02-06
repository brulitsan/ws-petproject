
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stock_market", "0004_rename_product_id_order_product"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="id",
            field=models.CharField(editable=False, primary_key=True, serialize=False),
        ),
    ]
