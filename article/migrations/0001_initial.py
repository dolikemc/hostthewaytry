# Generated by Django 2.1.3 on 2018-11-28 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('reviewed', models.BooleanField(default=False, editable=False)),
                ('deleted', models.BooleanField(default=False, editable=False)),
                ('text', models.TextField(blank=True, null=True)),
                ('picture', models.ImageField(blank=True, help_text='Picture of your place', upload_to='')),
                ('longitude', models.FloatField(blank=True, help_text='Where is your place (longitude)?', null=True)),
                ('latitude', models.FloatField(blank=True, help_text='Where is your place (latitude)?', null=True)),
                ('copyright', models.TextField()),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE,
                                           to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TextArticle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('reviewed', models.BooleanField(default=False, editable=False)),
                ('deleted', models.BooleanField(default=False, editable=False)),
                ('text', models.TextField()),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE,
                                           to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]