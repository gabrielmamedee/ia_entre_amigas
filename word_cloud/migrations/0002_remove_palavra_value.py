# Generated by Django 4.2 on 2023-05-30 03:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('word_cloud', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='palavra',
            name='value',
        ),
    ]
