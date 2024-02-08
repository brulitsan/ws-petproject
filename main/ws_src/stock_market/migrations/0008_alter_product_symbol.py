
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stock_market", "0007_rename_name_product_symbol"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="symbol",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
