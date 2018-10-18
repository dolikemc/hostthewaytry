# Generated by Django 2.1.1 on 2018-09-19 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('places', '0010_auto_20180918_2040'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, default=1.0, help_text='Price for the current category',
                                              max_digits=9)),
                ('currency', models.CharField(default='EUR', help_text='Currency ISO 3 Code', max_length=3)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('reviewed', models.BooleanField(default=False, editable=False)),
                ('deleted', models.BooleanField(default=False, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Towns',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of your town/area', max_length=200)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('reviewed', models.BooleanField(default=False, editable=False)),
                ('deleted', models.BooleanField(default=False, editable=False)),
            ],
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='Rooms',
        ),
        migrations.RemoveField(
            model_name='places',
            name='thumb_link',
        ),
        migrations.AddField(
            model_name='places',
            name='contact_type',
            field=models.CharField(choices=[('NO', "Unfortunately I'm personally not available"),
                                            ('CO', "I'll be in contact with my guests"),
                                            ('TI', "I'll spend time with my guests?"),
                                            ('PO', 'I can personally offer my guests'),
                                            ('NA', 'I could not answer this question')], default='NA',
                                   help_text='Waht kind of contact you can offer your guest?', max_length=2),
        ),
        migrations.AddField(
            model_name='places',
            name='laundry',
            field=models.BooleanField(default=False,
                                      help_text='Do you have laundry facilities at your house guests can use (washer/dryer)?'),
        ),
        migrations.AddField(
            model_name='places',
            name='meal_example',
            field=models.CharField(blank=True, help_text='Please describe a typical meal in your home', max_length=400),
        ),
        migrations.AddField(
            model_name='places',
            name='own_key',
            field=models.BooleanField(default=False, help_text='Do guests have their own key to the house?'),
        ),
        migrations.AddField(
            model_name='places',
            name='parking',
            field=models.BooleanField(default=False, help_text='Do you have parking at your house?'),
        ),
        migrations.AddField(
            model_name='places',
            name='price_breakfast',
            field=models.FloatField(help_text='Which is the average price for breakfast?', null=True),
        ),
        migrations.AddField(
            model_name='places',
            name='price_meal',
            field=models.FloatField(help_text='Which is the average price for dinner/lunch?', null=True),
        ),
        migrations.AddField(
            model_name='places',
            name='reviewed',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='places',
            name='separate_entrance',
            field=models.BooleanField(default=False, help_text='Is there a separate entrance to the house for guests?'),
        ),
        migrations.AddField(
            model_name='places',
            name='vegan',
            field=models.BooleanField(default=False, help_text='Do you serve vegan meal option?'),
        ),
        migrations.AddField(
            model_name='places',
            name='vegetarian',
            field=models.BooleanField(default=False, help_text='Do you serve vegetarian meal option?'),
        ),
        migrations.AddField(
            model_name='places',
            name='wifi',
            field=models.BooleanField(default=True, help_text='Do you have (free) WiFi at your house?'),
        ),
        migrations.AlterField(
            model_name='places',
            name='deleted',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='places',
            name='description',
            field=models.CharField(default='', help_text='What else would you like to tell your gusets?',
                                   max_length=500),
        ),
        migrations.AlterField(
            model_name='places',
            name='handicapped_enabled',
            field=models.BooleanField(default=False, help_text='Is your house suitable for handicapped guests?'),
        ),
        migrations.AlterField(
            model_name='places',
            name='latitude',
            field=models.FloatField(
                help_text='Where is your place (latitude)? Could be taken from the picture meta data', null=True),
        ),
        migrations.AlterField(
            model_name='places',
            name='longitude',
            field=models.FloatField(
                help_text='Where is your place (longitude)? Could be taken from the picture meta data', null=True),
        ),
        migrations.AlterField(
            model_name='places',
            name='meals',
            field=models.CharField(
                choices=[('NO', 'no meal at all'), ('BR', 'only breakfast'), ('BL', 'breakfast and lunch'),
                         ('BD', 'breakfast and dinner'), ('AL', 'breakfast, lunch and dinner')], default='NO',
                help_text='How many meals per day your serve?', max_length=2),
        ),
        migrations.AlterField(
            model_name='places',
            name='picture',
            field=models.ImageField(default='hosttheway.jpg', help_text='Picture of your place', upload_to=''),
        ),
        migrations.AddField(
            model_name='places',
            name='area',
            field=models.ForeignKey(default=None, help_text='Link to the available towns or areas', null=True,
                                    on_delete=django.db.models.deletion.CASCADE, to='places.Towns'),
        ),
    ]
