# Generated by Django 2.1.3 on 2018-11-28 09:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('places', '0034_auto_20181113_1323'),
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='textarticle',
            name='place',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='places.Place'),
            preserve_default=False,
        ),
    ]
