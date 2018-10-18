# Generated by Django 2.1.1 on 2018-10-17 10:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('places', '0026_auto_20181016_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='place',
            name='priority_category',
            field=models.CharField(choices=[('NA', 'No special category'), ('AW', 'Alwasy on top')], default='NA',
                                   max_length=2),
        ),
        migrations.AddField(
            model_name='place',
            name='priority_valid_until',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='place',
            name='priority_value',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]