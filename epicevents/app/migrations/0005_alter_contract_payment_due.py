# Generated by Django 4.1.4 on 2023-01-02 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_alter_event_support_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='payment_due',
            field=models.DateTimeField(),
        ),
    ]
