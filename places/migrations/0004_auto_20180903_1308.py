# Generated by Django 2.1.1 on 2018-09-03 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('places', '0003_auto_20180903_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='places',
            name='description',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='places',
            name='address',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='places.Adress'),
        ),
        migrations.AlterField(
            model_name='places',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='places',
            name='longitude',
            field=models.FloatField(null=True),
        ),
    ]
