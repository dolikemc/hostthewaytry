# Generated by Django 2.1.1 on 2018-10-17 10:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('places', '0028_auto_20181017_1248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='contact_first_name',
        ),
        migrations.RemoveField(
            model_name='place',
            name='contact_last_name',
        ),
        migrations.RemoveField(
            model_name='place',
            name='email',
        ),
        migrations.RemoveField(
            model_name='place',
            name='email_alt',
        ),
        migrations.RemoveField(
            model_name='place',
            name='private_bathroom',
        ),
        migrations.RemoveField(
            model_name='place',
            name='private_kitchen',
        ),
        migrations.RemoveField(
            model_name='place',
            name='room_add',
        ),
    ]