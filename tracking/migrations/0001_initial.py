# Generated by Django 2.2.7 on 2020-03-10 18:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tracking_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('safekey', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('graph_filename', models.CharField(default='Your_file_name', max_length=500)),
                ('graph_title', models.CharField(default='Your graph title', max_length=500)),
                ('graph_xlabel', models.CharField(default='x-axis label', max_length=500)),
                ('graph_ylabel', models.CharField(default='y-axis label', max_length=500)),
                ('graph_description', models.CharField(default='This is what you can see in this graph...', max_length=2000)),
                ('myX', models.CharField(max_length=500)),
                ('myY', models.CharField(max_length=500)),
                ('myError', models.CharField(max_length=500)),
                ('mySymbol', models.CharField(default='x', max_length=30)),
                ('myDate', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
