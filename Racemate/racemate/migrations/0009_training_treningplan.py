# Generated by Django 2.1.5 on 2019-01-24 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('racemate', '0008_auto_20190123_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='treningplan',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
