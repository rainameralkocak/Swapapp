# Generated by Django 5.0.6 on 2024-06-18 15:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_course_category_course_instructor'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='status',
            field=models.CharField(default='Pending', max_length=20),
        ),
        migrations.AddField(
            model_name='meeting',
            name='url',
            field=models.CharField(default=None, max_length=150),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 6, 18, 18, 13, 48, 259160)),
        ),
    ]
