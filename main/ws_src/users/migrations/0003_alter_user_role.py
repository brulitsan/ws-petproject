# Generated by Django 4.2.9 on 2024-01-29 15:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_alter_user_balance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("Пользователь", "Пользователь"),
                    ("Аналитик", "Аналитик"),
                    ("Администратор", "Администратор"),
                ],
                default="Пользователь",
                max_length=20,
            ),
        ),
    ]
