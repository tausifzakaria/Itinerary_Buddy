# Generated by Django 3.2.9 on 2022-05-31 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ItineraryAppManagement', '0015_rename_itineraries_itinerarie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itinerarie',
            name='state',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='ItineraryAppManagement.city'),
        ),
    ]
