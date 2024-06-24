# Generated by Django 5.0.6 on 2024-06-23 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagamento', '0002_remove_order_shipped_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='refund_granted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='order',
            name='refund_requested',
            field=models.BooleanField(default=False),
        ),
    ]
