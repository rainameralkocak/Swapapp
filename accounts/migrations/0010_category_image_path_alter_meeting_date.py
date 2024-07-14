# Generated by Django 5.0.6 on 2024-06-21 06:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_creditcard_card_icon_url_creditcard_card_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image_path',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 21, 9, 0, 15, 598492)),
        ),
    ]
