# Generated by Django 2.1.1 on 2018-09-21 14:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('places', '0013_auto_20180921_1653'),
    ]

    operations = [
        migrations.AlterField(
            model_name='places',
            name='picture',
            field=models.ImageField(default='hosttheway.jpg', help_text='Picture of your place', upload_to=''),
        ),
    ]