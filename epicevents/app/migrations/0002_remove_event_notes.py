# Generated by Django 4.1.4 on 2022-12-28 11:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='notes',
        ),
    ]
