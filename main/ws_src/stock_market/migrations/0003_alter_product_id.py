
import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stock_market", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="id",
            field=models.CharField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
