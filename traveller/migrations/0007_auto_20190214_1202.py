# Generated by Django 2.1.5 on 2019-02-14 11:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('traveller', '0006_auto_20181129_1316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='placeaccount',
            name='place',
        ),
        migrations.RemoveField(
            model_name='placeaccount',
            name='user',
        ),
        migrations.DeleteModel(
            name='PlaceAccount',
        ),
    ]