# Generated by Django 2.1.1 on 2018-09-03 11:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('places', '0005_auto_20180903_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='places',
            name='thumb_link',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='rooms',
            name='thumb_link',
            field=models.URLField(null=True),
        ),
    ]