# Generated by Django 5.0.6 on 2024-06-22 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loja', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='estoque',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
