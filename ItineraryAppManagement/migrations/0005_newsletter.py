# Generated by Django 4.0 on 2022-05-07 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ItineraryAppManagement', '0004_banner_itineraries_banner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=50)),
            ],
        ),
    ]