# Generated by Django 2.1.5 on 2019-01-23 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('racemate', '0007_auto_20190123_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='easy',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='training',
            name='interval',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='training',
            name='marathon',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='training',
            name='repetition',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='training',
            name='threshold',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='training',
            name='trainingday',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='training',
            name='walk',
            field=models.IntegerField(null=True),
        ),
    ]
