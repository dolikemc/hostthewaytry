# Generated by Django 2.1.5 on 2019-01-30 18:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='beds',
            new_name='adults',
        ),
        migrations.AddField(
            model_name='booking',
            name='kids',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
