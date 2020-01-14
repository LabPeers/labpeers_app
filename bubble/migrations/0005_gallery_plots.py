# Generated by Django 2.2.7 on 2020-01-13 17:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bubble', '0004_remove_graph_data_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery_Plots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myplots', models.ImageField(blank=True, null=True, upload_to='plots/')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]