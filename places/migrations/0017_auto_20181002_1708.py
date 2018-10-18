# Generated by Django 2.1.1 on 2018-10-02 15:08

from django.db import migrations, models
import places.image_filed_extend


class Migration(migrations.Migration):
    dependencies = [
        ('places', '0016_auto_20180925_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='places',
            name='description',
            field=models.CharField(blank=True, default='', help_text='What else would you like to tell your gusets?',
                                   max_length=500),
        ),
        migrations.AlterField(
            model_name='places',
            name='latitude',
            field=models.FloatField(blank=True,
                                    help_text='Where is your place (latitude)? Could be taken from the picture meta data',
                                    null=True),
        ),
        migrations.AlterField(
            model_name='places',
            name='longitude',
            field=models.FloatField(blank=True,
                                    help_text='Where is your place (longitude)? Could be taken from the picture meta data',
                                    null=True),
        ),
        migrations.AlterField(
            model_name='places',
            name='picture',
            field=places.image_filed_extend.ImageFieldExtend(default='hosttheway.jpg',
                                                             help_text='Picture of your place', upload_to=''),
        ),
    ]
