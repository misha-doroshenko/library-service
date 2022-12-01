# Generated by Django 4.1.3 on 2022-11-30 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payments", "0002_payment_status_payment_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="money_to_pay",
            field=models.DecimalField(
                decimal_places=2, default=0, max_digits=5
            ),
            preserve_default=False,
        ),
    ]
