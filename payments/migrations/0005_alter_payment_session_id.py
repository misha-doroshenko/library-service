# Generated by Django 4.1.3 on 2022-11-30 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0004_alter_payment_status_alter_payment_type"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="session_id",
            field=models.CharField(max_length=255),
        ),
    ]
