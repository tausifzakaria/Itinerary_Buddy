# Generated by Django 3.1 on 2022-05-23 18:10

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('ItineraryAppManagement', '0010_alter_itineraries_top_rated_itinerary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itineraries',
            name='long_description',
            field=tinymce.models.HTMLField(),
        ),
    ]