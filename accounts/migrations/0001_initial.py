# Generated by Django 2.2.7 on 2020-03-10 18:05

import accounts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import storages.backends.s3boto3


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', accounts.models.S3PrivateFileField(blank=True, default='default.jpg', null=True, storage=storages.backends.s3boto3.S3Boto3Storage(acl='private'), upload_to=accounts.models.upload_pic)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
