# Generated by Django 4.0.3 on 2024-04-08 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservationApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='bus',
        ),
    ]