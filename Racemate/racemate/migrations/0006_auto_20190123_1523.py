# Generated by Django 2.1.5 on 2019-01-23 14:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('racemate', '0005_pasttraining'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trainingelement',
            old_name='speed',
            new_name='time',
        ),
    ]
