# Generated by Django 2.2.7 on 2020-03-10 17:00

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tracking_data',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
