# Generated by Django 2.2.7 on 2020-02-19 20:02

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20200219_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to=accounts.models.upload_pic),
        ),
    ]
