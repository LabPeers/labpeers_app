# Generated by Django 2.2.7 on 2020-03-10 18:16

import bubble.models
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
            name='Graph_Data',
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
                ('myRadius', models.CharField(max_length=500)),
                ('myScale', models.FloatField(default=1, max_length=1)),
                ('myDate', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Gallery_Plots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plotname', models.CharField(default='NewPlot', max_length=200)),
                ('myDate', models.DateTimeField(auto_now=True)),
                ('myplots', models.ImageField(blank=True, null=True, upload_to=bubble.models.upload_plots)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
