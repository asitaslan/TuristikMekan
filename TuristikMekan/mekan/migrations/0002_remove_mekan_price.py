# Generated by Django 3.0.4 on 2020-08-07 11:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mekan', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mekan',
            name='price',
        ),
    ]
