# Generated by Django 4.1.4 on 2022-12-28 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_remove_event_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='notes',
            field=models.TextField(blank=True, max_length=200),
        ),
    ]
