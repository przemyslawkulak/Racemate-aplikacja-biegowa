# Generated by Django 2.1.5 on 2019-01-23 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('racemate', '0006_auto_20190123_1523'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='training',
            name='distance_total',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='training',
            name='time_total',
            field=models.IntegerField(null=True),
        ),
    ]
