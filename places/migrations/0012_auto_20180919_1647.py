# Generated by Django 2.1.1 on 2018-09-19 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('places', '0011_auto_20180919_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='places',
            name='area',
            field=models.ForeignKey(blank=True, help_text='Link to the available towns or areas', null=True,
                                    on_delete=django.db.models.deletion.CASCADE, to='places.Towns'),
        ),
        migrations.AlterField(
            model_name='places',
            name='price_breakfast',
            field=models.FloatField(blank=True, help_text='Which is the average price for breakfast?', null=True),
        ),
        migrations.AlterField(
            model_name='places',
            name='price_meal',
            field=models.FloatField(blank=True, help_text='Which is the average price for dinner/lunch?', null=True),
        ),
    ]
