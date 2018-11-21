# Generated by Django 2.1.3 on 2018-11-19 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('traveller', '0008_auto_20181119_2014'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='traveller',
            name='place_permission',
        ),
        migrations.AddField(
            model_name='placeaccount',
            name='traveller',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING,
                                    to='traveller.Traveller'),
        ),
    ]