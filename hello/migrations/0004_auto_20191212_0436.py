# Generated by Django 2.2.7 on 2019-12-12 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_graph_data_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='graph_data',
            name='id',
        ),
        migrations.AddField(
            model_name='graph_data',
            name='graph_filename',
            field=models.CharField(default='Your_file_name', max_length=500, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='graph_data',
            name='graph_title',
            field=models.CharField(default='Your graph title', max_length=500),
        ),
    ]
